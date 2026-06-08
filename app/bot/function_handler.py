from .generate_image import generateImage
from . import *
from ..services import *
from ..services.call_esp8266 import get_sensor_data

def callback_func(target: str, args: dict = None):    
    try:
        generate_arg_list = []
        for arg, value in args.items():
            if isinstance(value, int): 
                generate_arg_list.append(f'{arg} = {int(value)}')
            elif isinstance(value, str):
                generate_arg_list.append(f'{arg} = "{value}"')
            else:
                generate_arg_list.append(f'{arg} = {value}')

        result_set = {}
        call_function_str = f'result = {target}({", ".join(generate_arg_list)})'
        print("Call: ", call_function_str)
        exec(call_function_str, {f'{target}': eval(target)}, result_set)
        return result_set.get("result")
    except Exception as e:
        print(e)
        raise e