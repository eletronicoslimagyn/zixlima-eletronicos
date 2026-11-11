from PIL import Image
import os

# Nome do arquivo original (renomeie a imagem que você me mandou para logo_original.jpg e jogue na pasta do projeto)
input_file = 'logo_original.jpg'
output_file = 'logo_zixlima.png'

if os.path.exists(input_file):
    img = Image.open(input_file)
    width, height = img.size
    
    # Cortar a parte de baixo (onde fica o Instagram)
    # Vamos manter 75% da parte de cima da imagem
    new_height = int(height * 0.75)
    
    # Cortar
    cropped_img = img.crop((0, 0, width, new_height))
    
    # Salvar a nova imagem
    cropped_img.save(output_file)
    print(f"\n✅ Logo cortada com sucesso! Salva como: {output_file}")
    print("Agora você pode subir essa imagem para a pasta 'imagens' no GitHub.")
else:
    print(f"\n❌ Erro: Coloque a imagem original na pasta do projeto com o nome '{input_file}'")
