** az login --service-principal --username APP_ID --password PASSWORD --tenant TENANT_ID

https://pybit.es/articles/fastapi-app-as-azure-function-howto/
https://www.youtube.com/watch?v=HyCO6nMdxC0


<!-- CONTRUIR IMAGEN -->
docker build -f Dockerfile.backend -t nombre_de_tu_imagen .

<!-- CORRER IMAGEN -->
docker run -d -p 8000:8000 nombre_de_tu_imagen


<!-- SUBIR IMAGEN A DOCKER REGISTRY DE AZURE -->
docker login xxxxxxx.azurecr.io -u xxxx -p xxxxx
docker build -f Dockerfile.backend -t xxxxxx.azurecr.io/<nombre imagen>:<tag> .
docker push xxxxxx.azurecr.io/<nombre imagen>:<tag>



