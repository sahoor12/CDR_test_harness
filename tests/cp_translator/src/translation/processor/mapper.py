import copy
import json
import logging
import sys

from exceptions import MapConfigException, WorkInterrupt

from translation.processor.mapper_validator import MapperValidator

logger = logging.getLogger(__name__)

SUPPORTED_MAP_FUNCTIONS = {
    'map_key': ['result_key'],
    'split': [],
    'concatenate': ['input_keys', 'result_key'],
    'map_value': ['map_config'],
    'map_x_else_y': ['x', 'y', 'result_key']
}

def get_mapping_config():
    try:
        import os
        with open('/home/rasmitasahoo/Office/CDR/test-harness/tests/cp_translator/src/translation/processor/mapping.json', 'r') \
                as mapping_file:
            map_config = json.load(mapping_file)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        logger.error(
            "Missing mapping configuration.  Please supply a valid mapping configuration file which contains json.")
        raise Exception()
    return map_config


def init_mapper():
    try:
        mapping_config = get_mapping_config()
        return Mapper(mapping_config, logger)
    except (Exception, MapConfigException):
        sys.exit(1)
    except Exception as exc:
        logger.error('Mapping initialization failed.', exc_info=True)
        sys.exit(1)


class Mapper:
    """a class for translating documents from one format to another"""

    def __init__(self, mapping_config, logger):
        self.logger = logger or logging.getLogger(__name__)
        self.validate_config(mapping_config)
        self.mapping_config = mapping_config

    def validate_config(self, mapping_config):
        if not mapping_config:
            self.logger.warning('Mapping configuration is empty.  No translation will take place.')
        if not isinstance(mapping_config, list):
            exc = MapConfigException('Mapping configuration is of an unexpected type.')
            self.logger.error(exc)
            raise exc
        for item in mapping_config:
            self.validate_config_attribute(item)

    def validate_config_attribute(self, map_config_item):
        try:
            if not isinstance(map_config_item, list):
                raise MapConfigException(
                    'Value for mapping config attribute {} is of an unexpected type.'.format(map_config_item))
            if not isinstance(map_config_item[0], str):
                raise MapConfigException(
                    'Value for mapping config attribute {} contains an unexpected type.'.format(map_config_item))
            if map_config_item[0] not in SUPPORTED_MAP_FUNCTIONS:
                raise MapConfigException(
                    'The mapping function named, {}, is not a recognized mapping function.  {}'.format(
                        map_config_item[0], map_config_item))
            for required_kwarg in SUPPORTED_MAP_FUNCTIONS[map_config_item[0]]:
                if required_kwarg not in map_config_item[1]:
                    raise MapConfigException(
                        'Mapping configuration error: The key word parameter, {}, for map function, {},'
                        ' is required. config_item: {}'.format(required_kwarg, map_config_item[0], map_config_item))
        except Exception as exc:
            msg = "Encountered problem validating mapping configuration.  map_config_item: {}".format(map_config_item)
            self.logger.error(exc, exc_info=True)
            raise MapConfigException(msg) from exc

    def map(self, data_dict):
        final_result = list()
        work_stack = list()
        work_stack.append(data_dict)
        while work_stack:
            self.do_map_work(work_stack, final_result)
        return final_result[0]

    def do_map_work(self, work_stack, final_result):
        if not work_stack:
            return
        work_item = work_stack.pop()
        for map_func_config in self.mapping_config:
            try:
                self.apply_map_function(work_stack, work_item, map_func_config)
            except AttributeError:
                continue
            except WorkInterrupt:
                return
        final_result.append(work_item)

    def apply_map_function(self, work_stack, work_item, func_config):
        function_to_apply = getattr(self, func_config[0])
        if function_to_apply:
            function_to_apply(work_stack, work_item, **func_config[1])
        else:
            msg = "Unknown mapping function, {}." \
                  "\nfunction config: {}"
            self.logger.warning(msg.format(func_config[0], func_config))

    @staticmethod
    def map_key(work_stack, work_item, **kwargs):
        key = kwargs.get('key')
        result_key = kwargs.get('result_key')

        if not work_item:
            return

        if not key or not result_key:
            msg = "Key word parameters, 'key' and 'result_key', are required in the configuration for the 'map_key' " \
                  "translation function."
            raise MapConfigException(msg)

        if key not in work_item:
            return

        value = work_item.pop(key)
        work_item[result_key] = value

    @staticmethod
    def split(work_stack, work_item, **kwargs):
        key = kwargs.get('key')
        core_document_attributes = kwargs.get('core_document_attributes')

        if not MapperValidator.is_valid_split_config(work_item, key, core_document_attributes):
            return
        function_name = sys._getframe().f_code.co_name
        value_copy = copy.deepcopy(work_item[key])
        top_level_item_copy = copy.deepcopy(work_item)
        # Need to verify if core attributes present before adding top doc
        # to work_stack,function name acts as trigger to verify if that doc already in process

        if not function_name in work_item.keys():
            if MapperValidator.validate_core_attributes(core_document_attributes, work_item):
                top_level_item_copy.pop(key)
                top_level_item_copy[function_name] = key
                work_stack.append(top_level_item_copy)
        work_item[function_name] = key
        first_key_value = value_copy.pop()

        if type(first_key_value) == dict:
            work_item.pop(key)
            work_item.update(first_key_value)
        else:
            work_item[key] = first_key_value
        # Add doc only if all attributes satified in LinkedRemaAssortments
        if MapperValidator.validate_core_attributes(core_document_attributes, first_key_value):
            work_stack.append(work_item)
        if value_copy:
            next_work_item = copy.deepcopy(work_item)
            next_work_item[key] = value_copy
            work_stack.append(next_work_item)
        raise WorkInterrupt()

    @staticmethod
    def concatenate(work_stack, work_item, **kwargs):
        if not work_item:
            return
        result_key = kwargs.get('result_key')
        input_keys = kwargs.get('input_keys', [])
        input_values = []
        separator = kwargs.get('separator', '')
        if not isinstance(input_keys, list) or not input_keys:
            msg = "Key word parameter, 'input_keys', is required in the configuration " \
                  "for the 'concatenate' translation function.  It must have a list value."
            raise MapConfigException(msg)

        for key in input_keys:
            value = work_item.get(key)
            if value:
                input_values.append(value)
        if len(input_values) != len(input_keys):
            new_value = None
        else:
            new_value = separator.join(input_values)

        work_item[result_key] = new_value

    @staticmethod
    def map_value(work_stack, work_item, **kwargs):
        if not work_item:
            return
        try:
            map_config = kwargs['map_config']
            key = kwargs['key']
        except AttributeError:
            msg = "Key work parameters, 'map_config' and 'key', are required in the configuration " \
                  "for the 'map_value' translation function."
            raise MapConfigException(msg)
        if not map_config or not key or key not in work_item:
            return
        value = work_item.get(key)
        if not value:
            return
        new_value = map_config.get(value, None)
        work_item[key] = new_value

    @staticmethod
    def map_x_else_y(work_stack, work_item, **kwargs):
        if not work_item:
            return
        try:
            x = kwargs['x']
            y = kwargs['y']
            result_key = kwargs['result_key']
        except AttributeError:
            msg = "Key word parameters, 'x', 'y', and 'result_key', are required in the configuration " \
                  "for the 'map_x_else_y' translation function."
            raise MapConfigException(msg)
        if not x or not y:
            return
        x_value = work_item.get(x)
        y_value = work_item.get(y)
        if x_value:
            work_item.pop(x)
            work_item[result_key] = x_value
        elif y_value:
            work_item.pop(y)
            work_item[result_key] = y_value
        else:
            return
