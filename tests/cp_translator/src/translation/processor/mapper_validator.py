import logging


class MapperValidator:

    def validate_core_attributes(core_document_attributes, first_key_value):
        if not core_document_attributes or len(core_document_attributes) == 0:
            return False
        is_valid = True
        # Need to make sure the attributes present before proceeding
        for corekey in core_document_attributes:
            has_array = False
            has_field = False
            if isinstance(corekey, list):
                for attr in corekey:
                    has_array = True
                    if attr in first_key_value.keys():
                        has_field = True
                        break
            # all other keys should be present
            else:
                if not corekey in first_key_value.keys():
                    logging.warning("Key from Core attributes does not exist" + str(corekey))
                    is_valid = False
            if has_array and not has_field:
                logging.warning("Key from Core attributes does not exist" + str(corekey))
                is_valid = False
        return is_valid

    def is_valid_split_config(work_item, key, core_document_attributes=None):
        is_valid = True
        if not work_item:
            is_valid = False

        elif key not in work_item.keys() or not isinstance(work_item[key], list):
            is_valid = False

        elif not work_item[key]:
            is_valid = False

        return is_valid
