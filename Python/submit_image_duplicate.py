from flask import Blueprint , render_template,request,redirect
import torch
import trainer
import pickle_trainer
from torchvision.transforms import transforms
from PIL import Image

submit_image = Blueprint("submit_image" , __name__ , static_folder="static" , template_folder="templates")

trainer_instance = pickle_trainer.Trained.load('saved_trainer.pkl')

# Load the saved model
model_path = './classification_model.pth'
arch0 = [32, 32, 64, 64, 64]
loaded_model = trainer.Model1(input_channels=1, output_channels=2, arch=arch0, size=(256, 256)).to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))
loaded_model.load_state_dict(torch.load(model_path))
loaded_model.eval()

@submit_image.route("/image" ,methods=['GET','POST'])
@submit_image.route("/",methods=['GET','POST'])
def check():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if request.method == 'POST':
        img = request.files['image']

        image = Image.open(img).convert("L")

        image_transformation = trainer.transforms.Compose([  
            trainer.transforms.Resize((256,256)),
            trainer.transforms.ToTensor(),
        ])

        img = image_transformation(image).unsqueeze(0).to(device)
        # passing to model
        prediction = trainer_instance.model.eval()(img)
        result = torch.argmax(prediction, dim=1).item()
        if result == 1 :
            message = " Parkinson's Positive "
            return render_template("Pages/upload.html" , message=message)
        elif result == 0 :
            message = " Parkinson's Negative"
            return render_template("Pages/upload.html" , message=message)
        
    return redirect("/upload")
