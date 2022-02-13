import torch
import torchvision.transforms as transforms
from PIL import Image
import torch.nn as nn
from torchvision.models import vgg19
import torch.optim as optim
from tqdm import tqdm
from config import is_processing


def return_image(original_image_path, style_image_path, bot, message):
    is_processing.change(True)
    # device = torch.device("cuda" if (torch.cuda.is_available()) else 'cpu')
    device = 'cpu'

    def image_loader(path):
        image = Image.open(path)
        loader = transforms.Compose([transforms.Resize((256, 256)),
                                     transforms.ToTensor()])
        image = loader(image).unsqueeze(0)
        return image.to(device, torch.float)

    original_image = image_loader(original_image_path)
    style_image = image_loader(style_image_path)
    generated_image = original_image.clone().requires_grad_(True)

    class VGG(nn.Module):
        def __init__(self):
            super(VGG, self).__init__()
            self.req_features = ['0', '5', '10', '19', '28']
            self.model = vgg19(pretrained=True).features[:29]

        def forward(self, x):
            features = []
            for layer_num, layer in enumerate(self.model):
                x = layer(x)
                if (str(layer_num) in self.req_features):
                    features.append(x)

            return features

    def calc_content_loss(gen_feat, orig_feat):
        content_l = torch.mean((gen_feat - orig_feat) ** 2)
        return content_l

    def calc_style_loss(gen, style):
        batch_size, channel, height, width = gen.shape

        G = torch.mm(gen.view(channel, height * width), gen.view(channel, height * width).t())
        A = torch.mm(style.view(channel, height * width), style.view(channel, height * width).t())

        style_l = torch.mean((G - A) ** 2)
        return style_l

    def calculate_loss(gen_features, orig_feautes, style_featues):
        style_loss = content_loss = 0
        for gen, cont, style in zip(gen_features, orig_feautes, style_featues):
            content_loss += calc_content_loss(gen, cont)
            style_loss += calc_style_loss(gen, style)

        total_loss = content_weight * content_loss + style_weight * style_loss
        return total_loss

    model = VGG().to(device).eval()

    epoch = 50
    lr = 0.005
    content_weight = 1
    style_weight = 100

    optimizer = optim.Adam([generated_image], lr=lr)
    for e in tqdm(range(epoch)):
        gen_features = model(generated_image)
        orig_feautes = model(original_image)
        style_featues = model(style_image)

        total_loss = calculate_loss(gen_features, orig_feautes, style_featues)
        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()
        if e % 10 == 0:
            bot.send_message(message.chat.id, (str(int((e /epoch) * 100))) + "%")
    return generated_image
