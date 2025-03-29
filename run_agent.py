import argparse
import asyncio
import re
from metagpt.actions import Action, UserRequirement
from metagpt.context import Context
from metagpt.environment import Environment
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.roles.role import RoleReactMode
from metagpt.schema import Message
from tqdm import tqdm
from Script.Case_Analyst import find_case,Case_Description
from Script.proofreader import case_feedback3,compare_result,organize_case_feedback_content,organize_case_feedback_logic,organize_case_feedback_enlightening,oral_feedback,organize_refine,final_feedback_consistent,final_feedback_expression,final_refine
from Script.Topic_Researcher import topic_demonstrate,topic_expansion
from Script.Editor import case_organize,case_assemble3,case_assemble2
from Script.Narrator import case_change_style,oral_refine
from pathlib import Path
from pydantic import BaseModel


class dict_message(BaseModel):
    content: dict

class FindKeyCase(Action):
    name: str = "FindKeyCase"
    async def run(self, content: str):
        rsp = await find_case(content)
        return rsp

class GetDetailCase(Action):
    name: str = "GetDetailCase"
    async def run(self, content: str,case_dict:dict):
        rsp = await Case_Description(content,case_dict)
        return rsp


class CaseAnalyst(Role):
    name: str = "Case-Analyst-1"
    profile: str = "Case Analyst Agent"
    case_dict: dict_message = None
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._watch([UserRequirement,KeyCaseFeedback])
        self.set_actions([FindKeyCase,GetDetailCase])
    async def _think(self):
        lst_message = self.get_memories()[-1].content
        lst_role = self.get_memories()[-1].role
        if lst_message.startswith('是') and lst_role == "Proof Reader Agent":
            self.rc.todo = GetDetailCase()
        else:
            self.rc.todo = FindKeyCase()
    async def _act(self) -> Message:
        todo = self.rc.todo
        print(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        context = self.get_memories()
        Lines = context[0].content
        msg = None
        if todo.name == "FindKeyCase":
            rsp_text = await todo.run(Lines)
            mes = dict_message(content=rsp_text)
            self.case_dict = mes
            msg = Message(instruct_content=mes, role=self.profile, cause_by=type(todo), send_to=ProofReader)
        if todo.name == "GetDetailCase":
            rsp_text = await todo.run(Lines,self.case_dict.content)
            mes = dict_message(content=rsp_text)
            msg = Message(instruct_content=mes, role=self.profile, cause_by=type(todo))
        self.rc.env.publish_message(msg)
        return msg

class TopicDemonstrate(Action):
    name: str = "TopicDemonstrate"
    async def run(self, content: str,case_dict:dict):
        rsp = await topic_demonstrate(content,case_dict)
        return rsp

class TopicExpansion(Action):
    name: str = "TopicExpansion"
    async def run(self, content: str,case_dict:dict,demonstrate_dict:dict):
        rsp = await topic_expansion(content,case_dict,demonstrate_dict)
        return rsp

class TopicResearch(Role):
    name: str = "Topic-Research"
    profile: str = "Topic Research Agent"
    detail_case: dict = None
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._watch([GetDetailCase,TopicDemonstrate])
        self.set_actions([TopicDemonstrate,TopicExpansion])
    async def _think(self):
        lst_role = self.get_memories()[-1].role
        if lst_role == "Case Analyst Agent":
            self.rc.todo = TopicDemonstrate()
        else:
            self.rc.todo = TopicExpansion()
    async def _act(self) -> Message:
        todo = self.rc.todo
        print(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        context = self.get_memories()
        Lines = context[0].content
        if todo.name == "TopicDemonstrate":
            case_dict = context[-1].instruct_content.content
            self.detail_case = case_dict
            rsp_text = await todo.run(Lines,case_dict)
            mes = dict_message(content=rsp_text)
            msg = Message(instruct_content=mes, role=self.profile, cause_by=type(todo))
        else:
            case_dict = self.detail_case
            demonstrate_dict = context[-1].instruct_content.content
            rsp_text = await todo.run(Lines, case_dict,demonstrate_dict)
            mes = dict_message(content=rsp_text)
            msg = Message(instruct_content=mes, role=self.profile, cause_by=type(todo))
        self.rc.env.publish_message(msg)
        return msg

class KeyCaseFeedback(Action):
    name: str = "KeyCaseFeedback"
    async def run(self, content: str,case_dict:dict):
        rsp = await case_feedback3(content,case_dict)
        return rsp
class CaseOrganizeContent(Action):
    name: str = "CaseOrganizeContent"
    async def run(self, content: str,case_dict:dict,demonstrate_dict:dict,insight_dict:dict,organize_dict:dict):
        rsp = await organize_case_feedback_content(content,case_dict,demonstrate_dict,insight_dict,organize_dict)
        return rsp
class CaseOrganizeLogic(Action):
    name: str = "CaseOrganizeLogic"
    async def run(self, content: str,case_dict:dict,demonstrate_dict:dict,insight_dict:dict,organize_dict:dict):
        rsp = await organize_case_feedback_logic(content,case_dict,demonstrate_dict,insight_dict,organize_dict)
        return rsp

class OralFeedback(Action):
    name: str = "OralFeedback"
    async def run(self, organize_dict:dict,oral_dict:dict):
        rsp = await oral_feedback(organize_dict,oral_dict)
        return rsp


class FinalFeedbackConsistent(Action):
    name: str = "FinalFeedbackConsistent"
    async def run(self, content: str,final_text:str):
        rsp = await final_feedback_consistent(content,final_text)
        return rsp

class FinalFeedbackExpression(Action):
    name: str = "FinalFeedbackExpression"
    async def run(self, content: str,final_text:str):
        rsp = await final_feedback_expression(content,final_text)
        return rsp

class str_message(BaseModel):
    content: str

class RefineCompare(Action):
    name: str = "RefineCompare"
    async def run(self, content: str,final_text1:str,final_text2:str):
        rsp = await compare_result(content,final_text1,final_text2)
        return rsp


class ProofReaderFinal(Role):
    name: str = "Proof-Reader-Final"
    profile: str = "Proof Reader Final Agent"
    consistent_cnt:int = 0
    expression_cnt:int = 0
    final_text:str = ""
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._watch([CaseAssemble,FinalFeedbackRefine,RefineCompare])
        self.set_actions([FinalFeedbackConsistent,FinalFeedbackExpression,RefineCompare])

    async def _think(self):
        lst_role = self.get_memories()[-1].role
        lst_case_by = self.get_memories()[-1].cause_by
        lst_msg = self.get_memories()[-1].content
        if lst_case_by == "__main__.CaseAssemble":
            self.rc.todo = FinalFeedbackConsistent()
        elif lst_case_by == "__main__.FinalFeedbackRefine":
            self.rc.todo = RefineCompare()
        else:
            self.rc.todo = FinalFeedbackExpression()

    async def _act(self) -> Message:
        todo = self.rc.todo
        print(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        context = self.get_memories()
        Lines = context[0].content
        if todo.name == "FinalFeedbackConsistent":
            if self.consistent_cnt == 0:
                final_text = context[-1].content
                self.final_text = final_text
                mes2 = str_message(content=self.final_text)
                rsp_text = await todo.run(Lines,final_text)
                self.consistent_cnt += 1
                msg = Message(content=rsp_text, instruct_content=mes2,role=self.profile, cause_by=type(todo), send_to=FinalCompiler)
                self.rc.env.publish_message(msg)
                return msg
        if todo.name == "FinalFeedbackExpression":
            final_text = context[-1].instruct_content.content
            mes2 = str_message(content=self.final_text)
            rsp_text = await todo.run(Lines, final_text)
            if rsp_text == "是":
                self.expression_cnt += 1
                print("-------------------Final---------------------")
                f3 = open(Path(args.output_file), "a", encoding="utf-8", errors="ignore")
                f3.write(self.final_text+'\n')
                f3.close()
                print(self.final_text)
            else:
                self.expression_cnt += 1
                msg = Message(content=rsp_text, instruct_content=mes2, role=self.profile, cause_by=type(todo),
                              send_to=FinalCompiler)
                self.rc.env.publish_message(msg)
                return msg
        if todo.name == "RefineCompare":
            final_text2 = context[-1].instruct_content.content
            rsp_text = await todo.run(Lines,self.final_text,final_text2)
            if rsp_text == "讲稿2":
                self.final_text = final_text2
            mes2 = str_message(content=self.final_text)
            if self.expression_cnt == 0:
                msg = Message(instruct_content=mes2, role=self.profile, cause_by=type(todo),
                              send_to=ProofReaderFinal)
                self.rc.env.publish_message(msg)
                return msg
            else:
                print("-------------------Final---------------------")
                print(self.final_text)
                print("-------------------Final---------------------")
                f3 = open(Path(args.output_file), "a", encoding="utf-8", errors="ignore")
                f3.write(self.final_text+'\n')
                f3.close()
class FinalFeedbackRefine(Action):
    name: str = "FinalFeedbackRefine"
    async def run(self, final_text: str,final_feedback:str):
        rsp,flag = await final_refine(final_text,final_feedback)
        return rsp,flag
class FinalCompiler(Role):
    name: str = "Final-Compiler"
    profile: str = "Final Compiler Agent"
    save_oral_dict:dict = None
    start_content: bool = False
    start_logic:bool = False
    content_cnt:int = 0

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._watch([FinalFeedbackConsistent,FinalFeedbackExpression])
        self.set_actions([FinalFeedbackRefine])

    async def _act(self) -> Message:
        todo = self.rc.todo
        print(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        context = self.get_memories()
        feedback_text = context[-1].content
        final_text = context[-1].instruct_content.content
        if todo.name == "FinalFeedbackRefine":
            rsp_text,flag = await todo.run(final_text,feedback_text)
            mes2 = str_message(content=rsp_text)
            msg = Message(content=flag,instruct_content=mes2,role=self.profile, cause_by=type(todo), send_to=ProofReaderFinal)
            self.rc.env.publish_message(msg)
            return msg


class ProofReader(Role):
    name: str = "Proof-Reader-1"
    profile: str = "Proof Reader Agent"
    case_dict: dict = None
    case_demonstrate: dict = None
    case_expansion: dict = None
    case_organize_dict: dict = None
    save_oral_dict:dict = None
    start_content: bool = False
    start_logic:bool = False
    start_oral:bool = False
    content_cnt:int = 0
    logic_cnt:int = 0
    oral_cnt:int = 0
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._watch([FindKeyCase,CaseOrganize,CaseOrganizeRefine,OralRewrite,OralRefine])
        self.set_actions([KeyCaseFeedback,CaseOrganizeContent,CaseOrganizeLogic,OralFeedback])

    async def _think(self):
        lst_role = self.get_memories()[-1].role
        lst_case_by = self.get_memories()[-1].cause_by
        lst_msg = self.get_memories()[-1].content
        if lst_role == "Case Analyst Agent":
            self.rc.todo = KeyCaseFeedback()
        elif lst_case_by == "__main__.CaseOrganize" or (self.start_content and self.start_logic == False and lst_msg != ""):
            self.rc.todo = CaseOrganizeContent()
        elif ((lst_msg == "" and self.start_logic == False and self.start_content) or
              (self.start_logic and lst_role!="Oralisation Specialists Agent")):
            self.rc.todo = CaseOrganizeLogic()
        elif lst_role == "Oralisation Specialists Agent":
            self.rc.todo = OralFeedback()

    async def _act(self) -> Message:
        todo = self.rc.todo
        print(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        context = self.get_memories()
        Lines = context[0].content
        if todo.name == "KeyCaseFeedback":
            key_case = context[-1].instruct_content.content
            rsp_text = await todo.run(Lines,key_case)
            msg = Message(content=rsp_text, role=self.profile, cause_by=type(todo), send_to=CaseAnalyst)
            self.rc.env.publish_message(msg)
            return msg
        elif todo.name == "CaseOrganizeContent":
            context2 = self.get_memories()
            case_dict = context2[-4].instruct_content.content
            self.case_dict = case_dict
            case_demonstrate = context2[-3].instruct_content.content
            self.case_demonstrate = case_demonstrate
            case_expansion = context2[-2].instruct_content.content
            self.case_expansion = case_expansion
            if self.start_content == False:
                case_organize_dict = context2[-1].instruct_content.content
                self.case_organize_dict = case_organize_dict
                rsp_text = await todo.run(Lines,case_dict,case_demonstrate,case_expansion,case_organize_dict)
                mes = dict_message(content=rsp_text)
                self.start_content = True
                self.content_cnt += 1
            else:
                wrong_key = context2[-1].content
                wrong_key_list = wrong_key.split('<')
                case_organize_dict = context2[-1].instruct_content.content
                self.case_organize_dict = case_organize_dict
                new_case_dict = {key:self.case_dict[key] for key in wrong_key_list}
                new_case_demonstrate = {key:self.case_demonstrate[key] for key in wrong_key_list}
                new_case_expansion = {key:self.case_expansion[key] for key in wrong_key_list}
                new_case_organize_dict = {key:case_organize_dict[key] for key in wrong_key_list}
                return_dict = {}
                if self.content_cnt<2:
                    rsp_text = await todo.run(Lines, new_case_dict, new_case_demonstrate, new_case_expansion,
                                              new_case_organize_dict)
                    for key,value in self.case_dict.items():
                        if key in wrong_key_list:
                            return_dict[key] = rsp_text[key]
                        else:
                            return_dict[key] = "是"
                    mes = dict_message(content=return_dict)
                else:
                    for key,value in self.case_dict.items():
                            return_dict[key] = "是"
                    mes = dict_message(content=return_dict)
                self.content_cnt += 1

            msg = Message(instruct_content=mes, role=self.profile, cause_by=type(todo),send_to=Compiler)
            self.rc.env.publish_message(msg)
            return msg
        elif todo.name == "CaseOrganizeLogic":
            context2 = self.get_memories()
            if self.start_logic == False:
                case_organize_dict = context2[-1].instruct_content.content
                self.case_organize_dict = case_organize_dict
                rsp_text = await todo.run(Lines,self.case_dict,self.case_demonstrate,self.case_expansion,self.case_organize_dict)
                mes = dict_message(content=rsp_text)
                self.start_logic = True
                self.logic_cnt += 1
            else:
                wrong_key = context2[-1].content
                wrong_key_list = wrong_key.split('<')
                case_organize_dict = context2[-1].instruct_content.content

                if wrong_key == "":
                    mes2 = dict_message(content=self.case_organize_dict)
                    msg = Message(instruct_content=mes2, role=self.profile, cause_by=type(todo),
                                  send_to=OralisationSpecialists)
                    self.rc.env.publish_message(msg)
                    return msg

                self.case_organize_dict = case_organize_dict
                new_case_dict = {key: self.case_dict[key] for key in wrong_key_list}
                new_case_demonstrate = {key: self.case_demonstrate[key] for key in wrong_key_list}
                new_case_expansion = {key: self.case_expansion[key] for key in wrong_key_list}
                new_case_organize_dict = {key: case_organize_dict[key] for key in wrong_key_list}
                return_dict = {}
                if self.logic_cnt<2:
                    rsp_text = await todo.run(Lines, new_case_dict, new_case_demonstrate, new_case_expansion,
                                              new_case_organize_dict)
                    for key, value in self.case_dict.items():
                        if key in wrong_key_list:
                            return_dict[key] = rsp_text[key]
                        else:
                            return_dict[key] = "是"
                    mes = dict_message(content=return_dict)
                else:
                    for key, value in self.case_dict.items():
                        return_dict[key] = "是"
                    mes = dict_message(content=return_dict)
                self.logic_cnt += 1

            msg = Message(instruct_content=mes, role=self.profile, cause_by=type(todo),
                          send_to=Compiler)
            self.rc.env.publish_message(msg)
            return msg
        elif todo.name == "OralFeedback":
            context2 = self.get_memories()
            if self.start_oral == False:
                oral_dict = context2[-1].instruct_content.content
                self.save_oral_dict = oral_dict
                rsp_text = await todo.run( self.case_organize_dict,oral_dict)
                mes = dict_message(content=rsp_text)
                self.start_oral = True
                self.oral_cnt += 1
            else:
                wrong_key = context2[-1].content
                wrong_key_list = wrong_key.split('<')
                oral_dict = context2[-1].instruct_content.content
                self.save_oral_dict = oral_dict
                if wrong_key == "":
                    mes2 = dict_message(content=self.save_oral_dict)
                    msg = Message(instruct_content=mes2, role=self.profile, cause_by=type(todo),
                                  send_to=Compiler)
                    self.rc.env.publish_message(msg)
                    return msg
                new_case_organize_dict = {key: self.case_organize_dict[key] for key in wrong_key_list}
                new_oral_dict = {key: self.save_oral_dict[key] for key in wrong_key_list}
                return_dict = {}
                if self.oral_cnt < 2:
                    rsp_text = await todo.run(new_case_organize_dict, new_oral_dict)
                    for key, value in self.case_dict.items():
                        if key in wrong_key_list:
                            return_dict[key] = rsp_text[key]
                        else:
                            return_dict[key] = "是"
                    mes = dict_message(content=return_dict)
                else:
                    for key, value in self.case_dict.items():
                        return_dict[key] = "是"
                    mes = dict_message(content=return_dict)
                self.oral_cnt += 1

            msg = Message(instruct_content=mes, role=self.profile, cause_by=type(todo),
                          send_to=OralisationSpecialists)
            self.rc.env.publish_message(msg)
            return msg

class CaseOrganize(Action):
    name: str = "CaseOrganize"
    async def run(self, content: str,case_dict:dict,demonstrate_dict:dict,insight_dict:dict):
        rsp = await case_organize(content,case_dict,demonstrate_dict,insight_dict)
        return rsp

class CaseOrganizeRefine(Action):
    name: str = "CaseOrganizeRefine"
    async def run(self, content: str,case_dict:dict,demonstrate_dict:dict,insight_dict:dict,organize_dict:dict,feedback_dict:dict):
        new_dict,wrong_key = await organize_refine(content,case_dict,demonstrate_dict,insight_dict,organize_dict,feedback_dict)
        return new_dict,wrong_key
class CaseAssemble(Action):
    name: str = "CaseAssemble"
    async def run(self, content: str,oral_dict:dict):
        rsp = await case_assemble3(content,oral_dict)
        return rsp
class Compiler(Role):
    name: str = "Compiler"
    profile: str = "Compiler Agent"
    organize_dict: dict = None
    first_flag: bool = False
    final_text :str = ""
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._watch([TopicExpansion,CaseOrganizeContent,CaseOrganizeLogic,OralFeedback])
        self.set_actions([CaseOrganize,CaseAssemble,CaseOrganizeRefine])
    async def _think(self):
        lst_role = self.get_memories()[-1].role
        lst_cause_by = self.get_memories()[-1].cause_by
        if lst_cause_by == "__main__.OralFeedback":
            self.rc.todo = CaseAssemble()
        elif lst_role == "Topic Research Agent":
            self.rc.todo = CaseOrganize()
        elif lst_role == "Proof Reader Agent":
            self.rc.todo = CaseOrganizeRefine()
    async def _act(self) -> Message:
        todo = self.rc.todo
        print(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        context = self.get_memories()
        Lines = context[0].content
        if todo.name == "CaseOrganize":
            case_dict = context[1].instruct_content.content
            demonstrate_dict = context[2].instruct_content.content
            insight_dict = context[3].instruct_content.content
            rsp_text = await todo.run(Lines,case_dict,demonstrate_dict,insight_dict)
            mes = dict_message(content=rsp_text)
            msg = Message(instruct_content=mes, role=self.profile, cause_by=type(todo),send_to=ProofReader)
            self.organize_dict = rsp_text
            self.rc.env.publish_message(msg)
            return msg
        elif todo.name == "CaseAssemble":
            oral_dict = context[-1].instruct_content.content
            rsp_text = await todo.run(Lines,oral_dict)
            self.final_text = rsp_text
            msg = Message(content=rsp_text, role=self.profile, cause_by=type(todo),
                          send_to=ProofReaderFinal)
            self.rc.env.publish_message(msg)
            return msg
        elif todo.name == "CaseOrganizeRefine":
            feedback_dict = context[-1].instruct_content.content
            case_dict = context[1].instruct_content.content
            case_demonstrate = context[2].instruct_content.content
            case_expansion = context[3].instruct_content.content
            rsp_text, wrong_key = await todo.run(Lines, case_dict, case_demonstrate, case_expansion, self.organize_dict,
                                                                                         feedback_dict)
            self.organize_dict = rsp_text
            mes = dict_message(content=rsp_text)
            msg = Message(content=wrong_key,instruct_content=mes, role=self.profile, cause_by=type(todo), send_to=ProofReader)
            self.rc.env.publish_message(msg)
            return msg


class OralRewrite(Action):
    name: str = "OralRewrite"
    async def run(self, case_organize:dict):
        rsp = await case_change_style(case_organize)
        return rsp
class OralRefine(Action):
    name: str = "OralRefine"
    async def run(self,org_dict:dict,oral_dict:dict,feedback:dict):
        new_dict,wrong_key  = await oral_refine(org_dict,oral_dict,feedback)
        return new_dict,wrong_key


class OralisationSpecialists(Role):
    name: str = "OralisationSpecialists"
    profile: str = "Oralisation Specialists Agent"
    detail_case: dict = None
    oral_dict: dict = None
    organize_dict: dict = None
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._watch([CaseOrganizeLogic,OralFeedback])
        self.set_actions([OralRewrite,OralRefine])
    async def _think(self):
        lst_case_by = self.get_memories()[-1].cause_by
        if lst_case_by == "__main__.CaseOrganizeLogic":
            self.rc.todo = OralRewrite()
        elif lst_case_by == "__main__.OralFeedback":
            self.rc.todo = OralRefine()
    async def _act(self) -> Message:
        todo = self.rc.todo
        print(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        context = self.get_memories()
        msg = None
        Lines = context[0].content
        if todo.name == "OralRewrite":
            case_org = context[-1].instruct_content.content
            self.organize_dict = case_org
            rsp_text = await todo.run(case_org)
            self.oral_dict = rsp_text
            mes = dict_message(content=rsp_text)
            msg = Message(instruct_content=mes, role=self.profile, cause_by=type(todo),send_to=ProofReader)
            self.rc.env.publish_message(msg)
            return msg
        elif todo.name == "OralRefine":
            feedback_dict = context[-1].instruct_content.content
            rsp_text, wrong_key = await todo.run(self.organize_dict,self.oral_dict,feedback_dict)
            self.organize_dict = rsp_text
            mes = dict_message(content=rsp_text)
            msg = Message(content=wrong_key, instruct_content=mes, role=self.profile, cause_by=type(todo),
                          send_to=ProofReader)
            self.rc.env.publish_message(msg)
            return msg

async def main(Lines):
    context = Context()
    env = Environment(context=context)
    env.add_roles([CaseAnalyst(),ProofReader(),TopicResearch(),Compiler(),OralisationSpecialists(),ProofReaderFinal(),FinalCompiler()])
    env.publish_message(
        Message(content=Lines))
    while not env.is_idle:
        await env.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process text files and generate results.")
    parser.add_argument("input_file", type=str, help="Path to the input text file")
    parser.add_argument("output_file", type=str, help="Path to the output result file")
    args = parser.parse_args()
    print(f"Input file: {args.input_file}")
    print(f"Output file: {args.output_file}")
    input_path = Path(args.input_file)
    if not input_path.is_file():
        print(f"Error: Input file '{args.input_file}' does not exist.")
        exit(1)
    try:
        Lines = open(input_path, 'r', encoding='utf-8').read()
    except Exception as e:
        print(f"Error reading input file: {e}")
        exit(1)
    asyncio.run(main(Lines))
