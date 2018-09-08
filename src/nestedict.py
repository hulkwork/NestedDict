import copy


class Nested(object):
    def __init__(self, nest_dict, sep="."):
        """

        :param nest_dict:
        :param sep:
        """
        self.sep = sep
        if not isinstance(nest_dict, dict):
            raise TypeError("nest_dict is not a <type dict> (%s)" % type(nest_dict))
        self.nested_dict = copy.deepcopy(nest_dict)

    def __getitem__(self, item):
        """

        :param item:
        :return:
        """
        return self.__retrieve(item, self.nested_dict)

    def __contains__(self, item):
        """

        :param item:
        :return:
        """
        try:
            self.__retrieve(item, _dict=self.nested_dict)
            return True
        except:
            return False

    def __retrieve(self, key, _dict):
        """

        :param key:
        :param _dict:
        :return:
        """
        deep_keys = key.split(self.sep)
        if len(deep_keys) == 1:
            if key in _dict:
                return _dict[key]
            else:
                raise KeyError("%s not found" % key)
        else:
            if deep_keys[0] in _dict:
                return self.__retrieve(self.sep.join(deep_keys[1:]), _dict=_dict[deep_keys[0]])
            else:
                raise KeyError("%s not found" % key)

    def get(self, key, default=None):
        """

        :param key:
        :param default:
        :return:
        """
        if self.__contains__(key):
            return self.__getitem__(key)
        else:
            return default

    def r_dict(self, before_key=None):
        """

        :param before_key:
        :return:
        """
        if self.__contains__(before_key):
            if isinstance(self.__getitem__(before_key), dict):
                for key in self.__getitem__(before_key):
                    return self.r_dict(self.sep.join([before_key, key]))
            else:
                return before_key

    def keys(self):
        """

        :return:
        """
        res = []
        for key in self.nested_dict:
            if isinstance(self.nested_dict[key], dict):
                for bkey in self.__getitem__(key):
                    tmp_res = self.r_dict(self.sep.join([key, bkey]))
                    res.append(tmp_res)
            else:
                res.append(key)
        return res

    def values(self):
        """

        :return:
        """
        keys = self.keys()
        return [self.__getitem__(key) for key in keys]

    def explode(self):
        """

        :return:
        """
        keys = self.keys()
        return {key: self.__getitem__(key) for key in keys}

    def __eq__(self, other):
        """

        :param other:
        :return:
        """
        if isinstance(other, Nested):
            return self.explode() == other.explode()
        else:
            return False

    def max_deep(self):
        """

        :return:
        """
        long_keys = self.explode().keys()
        return max(map(lambda x: len(x.split(self.sep)), long_keys))

    def min_deep(self):
        """

        :return:
        """
        long_keys = self.explode().keys()
        return min(map(lambda x: len(x.split(self.sep)), long_keys))

    def dtypes(self, to_string=False):
        """

        :param to_string:
        :return:
        """
        explode = self.explode()
        if to_string:
            tmp = {}
            for key in explode:
                try:
                    tmp[key] = type(explode[key]).__name__
                except:
                    tmp[key] = str(type(explode[key]))
            return tmp
        else:
            return {key: type(explode[key]) for key in explode}

    def go_deep(self, _dict, key, value):
        """

        :param _dict:
        :param key:
        :param value:
        :return:
        """
        deep_key = key.split(self.sep)
        if len(deep_key) == 1:
            _dict[key] = value
            return _dict
        else:
            self.go_deep(_dict[deep_key[0]], self.sep.join(deep_key[1:]), value)

    def set(self, instance, value):
        """

        :param instance:
        :param value:
        :return:
        """
        if self.__contains__(instance):
            return self.go_deep(self.nested_dict, instance, value)

    def explode_plus(self):
        """

        :return:
        """
        explode = self.explode()
        res = copy.deepcopy(self.explode())
        for key in explode:
            if type(explode[key]) in [list, tuple]:
                del res[key]
                for i, item in enumerate(explode[key]):

                    if isinstance(item, dict):
                        tmp_nested = Nested(item, sep=self.sep)
                        tmp = tmp_nested.explode_plus()
                        for k in tmp:
                            res["%s.%d.%s" % (key, i, k)] = tmp[k]
                    else:
                        res["%s.%d" % (key, i)] = explode[key][i]
        return res

    def dtypes_plus(self, to_string=True):
        explode = self.explode_plus()
        if to_string:
            tmp = {}
            for key in explode:
                try:
                    tmp[key] = type(explode[key]).__name__
                except:
                    tmp[key] = str(type(explode[key]))
            return tmp
        else:
            return {key: type(explode[key]) for key in explode}
