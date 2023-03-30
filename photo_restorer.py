import replicate
from dotenv import load_dotenv
load_dotenv()

def predict_image(filename):
    
    model = replicate.models.get ("tencentarc/gfpgan")
    version = model.versions.get ("9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3")
    # https: //replicate.com/tencentarc/gfpgan/versions/9283608cc6b7be6b65a844983db012355fde4132009f99d976b2£0896856a3#input
    inputs = {
    #Lnout
    'img': open (filename, "rb"),
    # GFPGAN version. v1.3: better quality. v1.4: more details and better
    # 1dentlty.
    'version': "v1.4",
    # Rescaling factor
    'scale': 2,
    # https: //replicate.com/tencentarc/gfpgan/versions/9283608cc6b7be6b65a8e44983db012355de4132

    }

    output = version.predict(**inputs)
    print(output)
    return output

