from prompt.gpt_structure import generate_prompt, generate_with_response_parser, create_prompt_input
import sys

def run_evaluate_noc_nor(self_agent_id_number: str,
                      self_agent_description: str,
                      environment_summary: str,
                      action_history: str,
                      engine='gpt4',
                      logger=None):
    '''
    Ask agent to report the number of characters and resources in the game

    Input:
        self_agent_id_number: str,
        self_agent_description: str,
        environment_summary: str,
        action_history: str,
        engine: str,
        logger: Logger, 已有的logger类

    Output:
        number_of_character: str, agent's guess of character count
        number_of_resource: str, agent's guess of resource count
        thought: str, agent's thinking process
    '''

    gpt_param = {"max_tokens": 500,
                 "temperature": 0, "top_p": 1, "stream": False,
                 "frequency_penalty": 0, "presence_penalty": 0, "stop": None}

    prompt_template = "prompt_files/prompt_4_evaluate_noc_nor.txt"
    prompt_input = create_prompt_input(self_agent_id_number,
                      self_agent_description,
                      environment_summary,
                      action_history)

    def parse_output(gpt_response):
        thought = gpt_response.split('### Thinking:')[-1].split('### Number of Character:')[0].strip()
        num_char = gpt_response.split('### Number of Character:')[-1].split('### Number of Resource:')[0].strip().split('\n')[0].strip()
        num_resource = gpt_response.split('### Number of Resource:')[-1].strip().split('\n')[0].strip()
        return thought, num_char, num_resource

    prompt = generate_prompt(prompt_input, prompt_template, fn_name=sys._getframe().f_code.co_name)
    if engine == 'human':
        num_char = '0'
        num_resource = '0'
        thought = '这个是人类，不需要thought'

    else:
        thought, num_char, num_resource = generate_with_response_parser(prompt,
                                                                        gpt_param=gpt_param,
                                                                        parser_fn=parse_output,
                                                                        engine=engine,
                                                                        logger=logger,
                                                                        func_name='run_evaluate_noc_nor')

    return num_char, num_resource, thought


