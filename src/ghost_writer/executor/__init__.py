import os


class FunctionCall:
    @staticmethod
    def find(function_dict):
        class_name = function_dict["name"][0].capitalize() + function_dict["name"][1:]
        func_call_class = globals().get(class_name, None)
        if func_call_class:
            return func_call_class(**function_dict["kwargs"])
        else:
            raise ValueError(f"Invalid function call name: {class_name}")


class DeleteFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def __call__(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def __str__(self):
        return f"Delete file: {self.file_path}"


class UpdateFile:
    def __init__(self, file_path, contents):
        self.file_path = file_path
        self.contents = contents

    def __call__(self):
        with open(self.file_path, "w") as file:
            file.write(self.contents)

    def __str__(self):
        return f"Update file '{self.file_path}' with contents: {self.contents}"


class Inquire:
    def __init__(self, file_path):
        self.file_path = file_path

    def __call__(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                contents = file.read()
            return {"file_path": self.file_path, "contents": contents}
        else:
            return {"file_path": self.file_path, "contents": ""}

    def __str__(self):
        return f"Inquire contents of file: {self.file_path}"


class Executor:
    def __init__(self, function_calls):
        self.function_calls = [FunctionCall.find(fc) for fc in function_calls]

    def execute(self, confirm=True):
        results = []
        for func_call in self.function_calls:
            try:
                if confirm:
                    print(str(func_call))
                    user_input = input("Do you want to continue? (y/n) ")
                    if user_input.lower() != "y":
                        print("Skipping this function call.")
                        continue

                result = func_call()
                results.append(result)
            except Exception as e:
                print(f"Error executing function call: {e}")
        return results
