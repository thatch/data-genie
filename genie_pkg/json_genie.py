import json

from jinja2 import Template
import random
import string
import json

import time
from typing import NewType
import uuid
from datetime import datetime, timedelta
from utils import generate_email_id, generate_ip

def _current_milli_time(): return int(round(time.time() * 1000))

def random_integer(start, max):
    return random.randint(start, max)

def random_float(start, max, decimal_places):
    return round(random.uniform(start, max), decimal_places)

def random_string(length):
    return ''.join([random.choice(string.ascii_letters) for i in range(0, length)])

def random_string_with_special_chars(length):
    special = ["¢", "£", "¥"]
    random_chars = [random.choice(string.ascii_letters + ''.join(special)) for i in range(0, length - 1)]
    return ''.join([random.choice(special)] + random_chars)

def random_string_list(list_size, item_length):
    l = []
    for i in range(0, list_size):
        l.insert(0, ''.join([random.choice(string.ascii_letters) for i in range(0, item_length)])) 
    #json dumps is to get python list as json compatible string.
    return json.dumps(l)

def random_integer_list(list_size, start, max):
    l = []
    for i in range(0, list_size):
        l.insert(0, random_integer(start, max)) 
    return l

def random_bool():
    return random.choice(['true', 'false'])

def now_epoch():
    return _current_milli_time()

def guid():
    return str(uuid.uuid4())

def random_choice_of(choices) -> str:
    return str(random.choice(choices))

def random_email_id(width, domain) -> str:
    return generate_email_id(width, domain)

def random_ipv4() -> str:
    return generate_ip()

def date_with_format(format_string='%Y/%m/%d', delta_days=0):
    return (datetime.today() - timedelta(days=delta_days)).strftime(format_string)

JinjaTemplate = NewType('JinjaTemplate', Template)

def _add_template_functions(template: JinjaTemplate) -> JinjaTemplate:
    template.globals['random_integer'] = random_integer
    template.globals['random_float'] = random_float
    template.globals['random_string'] = random_string
    template.globals['random_string_with_special_chars'] = random_string_with_special_chars
    template.globals['random_string_list'] = random_string_list
    template.globals['now_epoch'] = now_epoch
    template.globals['random_bool'] = random_bool
    template.globals['random_integer_list'] = random_integer_list
    template.globals['guid'] = guid
    template.globals['random_choice_of'] = random_choice_of
    template.globals['date_with_format'] = date_with_format
    template.globals['random_email_id'] = random_email_id
    template.globals['random_ipv4'] = random_ipv4
    return template

def generate(template_string) -> str:
    '''
        Generate json data for the provided specification

        Args:
            template_string (str): Jinja template string

        Returns:
            data (str): Jinja template rendered.
    '''
    
    t = Template(template_string)
    return _add_template_functions(t).render()

def generate_with_custom_template_function(template: JinjaTemplate) -> str:
    '''
        Generate json data for the provided specification

        Args:
            template (Template): Jinja template

        Returns:
            data (str): Jinja template rendered.
    '''

    return _add_template_functions(template).render()

