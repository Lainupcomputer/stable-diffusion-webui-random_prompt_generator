import random
from ez_storage.ez_storage import Ez_Storage


class Generator:
    def __init__(self, storage):
        self.storage_container = storage
        self.chosen_prompts = []
        self.positive_str_output = ""
        self.negative_str_output = ""

    def run(self, nsfw=False, check_for_duplicates=False):
        self.positive_str_output = ""
        self.negative_str_output = ""
        if nsfw:
            prompt_dict = "nsfw_registered_prompts"
        else:
            prompt_dict = "sfw_registered_prompts"

        try:
            for x in self.storage_container.get_storage(mode="a", obj=prompt_dict):
                for k, v in x.items():
                    prompts = self.storage_container.get_storage(mode="l", obj=k)
                    for i in range(int(v)):
                        self.chosen_prompts.append(random.choice(prompts))

            if check_for_duplicates:
                self.chosen_prompts = set(self.chosen_prompts)

            _str_pos = ""
            if self.storage_container.get_storage(mode="o", obj="Settings", data="enable_static_positive"):
                try:
                    for x in self.storage_container.get_storage(mode="l", obj="static_positive"):
                        _str_pos += x + ", "
                except KeyError:
                    _str_pos = ""

            for x in self.chosen_prompts:
                _str_pos += x + ", "
            self.positive_str_output = _str_pos

            _str_neg = ""
            if self.storage_container.get_storage(mode="o", obj="Settings", data="enable_static_negative"):
                try:
                    for x in self.storage_container.get_storage(mode="l", obj="static_negative"):
                        _str_neg += x + ", "
                except KeyError:
                    _str_neg = ""

                self.negative_str_output = _str_neg

        except KeyError as e:
            print(f"ERROR:{e}")

    def get_positive_str(self):
        return self.positive_str_output[:-2]

    def get_negative_str(self):
        return self.negative_str_output[:-2]


if __name__ == "__main__":
    g = Generator(Ez_Storage("./default.ezs"))
    g.run(nsfw=False, check_for_duplicates=True)
    print(f"NR:{len(g.chosen_prompts)}")
    print(f"POSITIVE_OUTPUT={g.get_positive_str()}")
    print(f"Negative_OUTPUT={g.get_negative_str()}")
