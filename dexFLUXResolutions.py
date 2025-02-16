import os
import json
import torch  # Используем PyTorch для создания тензоров

class dexFLUXResolutions:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        cls.size_sizes, cls.size_dict = read_sizes()
        return {
            'required': {
                'size_selected': (cls.size_sizes,),  # Выбор предопределённого разрешения
                'multiply_factor': ("INT", {"default": 1, "min": 1}),  # Коэффициент умножения
                'manual_width': ("INT", {
                    "default": 0,  # Значение по умолчанию
                    "min": 0,  # Минимальное значение
                }),
                'manual_height': ("INT", {
                    "default": 0,  # Значение по умолчанию
                    "min": 0,  # Минимальное значение
                }),
            }
        }

    RETURN_TYPES = ("INT", "INT", "LATENT")  # Добавляем выход LATENT
    RETURN_NAMES = ("width", "height", "latent_size")
    FUNCTION = "return_res"
    OUTPUT_NODE = False
    CATEGORY = "image"

    def return_res(self, size_selected, multiply_factor, manual_width, manual_height):
        # Определяем ширину и высоту изображения
        if manual_width > 0 and manual_height > 0:
            width = manual_width * multiply_factor
            height = manual_height * multiply_factor
            name = "Custom Size"
        else:
            selected_info = self.size_dict[size_selected]
            width = selected_info["width"] * multiply_factor
            height = selected_info["height"] * multiply_factor
            name = selected_info["name"]

        # Рассчитываем размеры латентного пространства (обычно делим на 8)
        latent_width = width // 8
        latent_height = height // 8

        # Создаём пустой тензор с формой [1, 4, latent_height, latent_width] (тип float32)
        latent_tensor = torch.zeros((1, 4, latent_height, latent_width), dtype=torch.float32)

        # Подготавливаем словарь для латентных данных
        latent_size = {"samples": latent_tensor}

        return (width, height, latent_size)

def read_sizes():
    p = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(p, 'sizes.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
    size_sizes = [f"{key} - {value['name']}" for key, value in data['sizes'].items()]
    size_dict = {f"{key} - {value['name']}": value for key, value in data['sizes'].items()}
    return size_sizes, size_dict

# Функция регистрации ноды
NODE_CLASS_MAPPINGS = {
    "dexFLUXResolutions": dexFLUXResolutions
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "dexFLUXResolutions": "DEX FLUX Resolutions"
}