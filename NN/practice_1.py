import torch
from torch import nn
import numpy as np

#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def function01(tensor: torch.Tensor, count_over: str) -> torch.Tensor:
    if count_over == 'rows':
        dim = 1
    if count_over == 'columns':
        dim = 0
    return tensor.mean(dim=dim)

def function02(tensor: torch.Tensor):
    num = tensor.shape[1]
    weights = torch.rand(num, dtype=torch.float32, requires_grad=True)
    return weights

def function03(x: torch.Tensor, y: torch.Tensor):
    weights = torch.rand(x.shape[1], requires_grad=True)
    mse = torch.tensor([2.0])
    i = 1
    while mse.item() >= 1:
        y_pred = torch.matmul(x, weights)
        mse = torch.mean((y_pred - y) ** 2)

        print(f'MSE на шаге {i} {mse.item():.5f}')

        mse.backward()

        step_size = 0.01
        with torch.no_grad():
            weights -= weights.grad * step_size

        weights.grad.zero_()
        i += 1

    return weights

# x = torch.tensor([[1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [4.0, 5.0]])  # Пример данных (4 объекта, 2 признака)
# y = torch.tensor([2.0, 3.0, 4.0, 5.0])  # Пример целевых значений
#
# weights = function03(x, y)
# print(weights)


def function04(x: torch.Tensor, y: torch.Tensor):
    layer = nn.Linear(in_features=x.shape[1], out_features=1)
    mse = torch.tensor([2.0])
    i = 1
    while mse.item() >= 0.3:
        y_pred = layer(x).ravel()
        print(y_pred)
        mse = torch.mean((y_pred - y) ** 2)

        print(f'MSE на шаге {i} {mse.item():.5f}')

        mse.backward()

        step_size = 0.01
        with torch.no_grad():
            layer.weight -= layer.weight.grad * step_size
            layer.bias -= layer.bias.grad * step_size

        layer.zero_grad()
        i += 1

    return layer

# x = torch.tensor([[1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [4.0, 5.0]])  # Пример данных (4 объекта, 2 признака)
# y = torch.tensor([2.0, 3.0, 4.0, 5.0])  # Пример целевых значений
#
# layer = function04(x, y)
# print(layer)