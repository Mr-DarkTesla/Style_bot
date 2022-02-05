import torch
import torchvision.transforms as transforms
from PIL import Image
import torch.nn as nn
import torchvision.models as models
import torch.optim as optim
from tqdm import tqdm
from config import is_processing


# # Loading the original and the style image
# original_image = image_loader('house.png')
# style_image = image_loader('Picasso.png')

def return_image(original_image_path, style_image_path):
    is_processing.change(True)

    #Loadung the model vgg19 that will serve as the base model
    model=models.vgg19(pretrained=True).features
    #Assigning the GPU to the variable device
    #device=torch.device("cuda" if (torch.cuda.is_available()) else 'cpu')
    device = 'cpu'
    #defing a function that will load the image and perform the required preprocessing and put it on the GPU
    def image_loader(path):
        image=Image.open(path)
        #defining the image transformation steps to be performed before feeding them to the model
        loader=transforms.Compose([transforms.Resize((256,256)), transforms.ToTensor()])
        #The preprocessing steps involves resizing the image and then converting it to a tensor
        image=loader(image).unsqueeze(0)
        return image.to(device,torch.float)

    # # Loading the original and the style image
    original_image = image_loader(original_image_path)
    style_image = image_loader(style_image_path)

    #Creating the generated image from the original image
    generated_image=original_image.clone().requires_grad_(True)


    # Defining a class that for the model
    class VGG(nn.Module):
        def __init__(self):
            super(VGG, self).__init__()
            self.req_features = ['0', '5', '10', '19', '28']
            # Since we need only the 5 layers in the model so we will be dropping all the rest layers from the features of the model
            self.model = models.vgg19(pretrained=True).features[:29]  # model will contain the first 29 layers

        # x holds the input tensor(image) that will be feeded to each layer
        def forward(self, x):
            # initialize an array that wil hold the activations from the chosen layers
            features = []
            # Iterate over all the layers of the mode
            for layer_num, layer in enumerate(self.model):
                # activation of the layer will stored in x
                x = layer(x)
                # appending the activation of the selected layers and return the feature array
                if (str(layer_num) in self.req_features):
                    features.append(x)

            return features


    def calc_content_loss(gen_feat,orig_feat):
        #calculating the content loss of each layer by calculating the MSE between the content and generated features and adding it to content loss
        content_l=torch.mean((gen_feat-orig_feat)**2)
        return content_l


    def calc_style_loss(gen, style):
        # Calculating the gram matrix for the style and the generated image
        batch_size, channel, height, width = gen.shape

        G = torch.mm(gen.view(channel, height * width), gen.view(channel, height * width).t())
        A = torch.mm(style.view(channel, height * width), style.view(channel, height * width).t())

        # Calcultating the style loss of each layer by calculating the MSE between the gram matrix of the style image and the generated image and adding it to style loss
        style_l = torch.mean((G - A) ** 2)
        return style_l

    def calculate_loss(gen_features, orig_feautes, style_featues):
        style_loss = content_loss = 0
        for gen, cont, style in zip(gen_features, orig_feautes, style_featues):
            # extracting the dimensions from the generated image
            content_loss += calc_content_loss(gen, cont)
            style_loss += calc_style_loss(gen, style)

        # calculating the total loss of e th epoch
        total_loss = alpha * content_loss + beta * style_loss
        return total_loss

    #Load the model to the GPU
    model=VGG().to(device).eval()

    #initialize the paramerters required for fitting the model
    epoch=50
    lr=0.005
    alpha=8
    beta=70

    #using adam optimizer and it will update the generated image not the model parameter
    optimizer=optim.Adam([generated_image],lr=lr)
    for e in tqdm(range(epoch)):
        # extracting the features of generated, content and the original required for calculating the loss
        gen_features = model(generated_image)
        orig_feautes = model(original_image)
        style_featues = model(style_image)

        # iterating over the activation of each layer and calculate the loss and add it to the content and the style loss
        total_loss = calculate_loss(gen_features, orig_feautes, style_featues)
        # optimize the pixel values of the generated image and backpropagate the loss
        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()
        # print the image and save it after each 100 epoch
        # if (e % 100 == 0):
        #     print(total_loss)
        #     save_image(generated_image, "./images/gen" + str(e//100) + ".png")

    return generated_image



















