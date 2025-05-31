	Executável:

		O aplicativo já possui uma build com um executável em: AppCage\src\dist\main\WheelCageApp.exe

	Código fonte:
		Para rodar o código fonte e consequentemente o aplicativo sem ser via executável buildado deve-se:
Ter o python 3.13.3 ou superior instalado e pip versão 25.0.1 ou superior.
Rodar na pasta AppCage o comando python -m venv venv para criar uma ambiente virtual com o nome “venv”.
Acessar o ambiente virtual com .\venv\Scripts\activate.
Acessar a pasta src cd .\src\ e instalar os pacotes com pip install -r ..\requirements.txt.
A partir disso já é possível rodar o aplicativo com python .\main.py ou gerar a build e executavel com pyinstaller .\main.spec e rodar o executável em AppCage\src\dist\main\WheelCageApp.exe
