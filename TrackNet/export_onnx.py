import torch
import onnx
from model import BallTrackerNet

# Load the state dict
state_dict = torch.load('model_best.pt')

# Create an instance of your model
model = BallTrackerNet()

# Load the state dict into your model
model.load_state_dict(state_dict)
model.eval()

# Create input tensor
input_shape = (1, 9, 360, 640)  # Shape is (batch_size, channels, height, width)
input_tensor = torch.randn(input_shape)

# Export to ONNX
output_path = 'model.onnx'
# torch.onnx.export(model,
#                   input_tensor,
#                   output_path,
#                   export_params=True,
#                   opset_version=11,
#                   do_constant_folding=True,
#                   input_names=['input'],
#                   output_names=['output'],
#                   dynamic_axes={'input': {0: 'batch_size'},
#                                 'output': {0: 'batch_size'}})
torch.onnx.export(model,
                  input_tensor,
                  output_path,
                  verbose=False,
                  input_names=['input'],
                  output_names=['output'],
                  export_params=True,
                  )
# Verify the exported model
onnx_model = onnx.load(output_path)
onnx.checker.check_model(onnx_model)

print(f"Model has been successfully exported to {output_path} and passed the ONNX checker.")