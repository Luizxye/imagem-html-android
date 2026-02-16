import base64
from io import BytesIO

from kivy.lang import Builder
from kivy.core.clipboard import Clipboard

from kivymd.app import MDApp

from plyer import filechooser

from PIL import Image


KV = '''
MDBoxLayout:
    orientation: "vertical"
    spacing: dp(10)
    padding: dp(15)

    MDTopAppBar:
        title: "Imagem → HTML"

    FitImage:
        id: preview
        source: ""
        size_hint_y: 0.5

    MDLabel:
        id: status
        text: "Status: Nenhuma imagem selecionada"
        halign: "center"

    MDRaisedButton:
        text: "Selecionar imagem"
        on_release: app.selecionar_imagem()

    MDRaisedButton:
        text: "Converter"
        on_release: app.converter()

    MDRaisedButton:
        text: "Copiar HTML"
        on_release: app.copiar()
'''


class AppPrincipal(MDApp):

    caminho = None
    html = ""

    def build(self):

        self.theme_cls.primary_palette = "Blue"

        return Builder.load_string(KV)

    def selecionar_imagem(self):

        filechooser.open_file(
            on_selection=self.arquivo_selecionado,
            filters=[("Imagens", "*.png", "*.jpg", "*.jpeg")]
        )

    def arquivo_selecionado(self, selection):

        if selection:

            self.caminho = selection[0]

            self.root.ids.preview.source = self.caminho

            self.root.ids.status.text = "Imagem selecionada"

    def converter(self):

        if not self.caminho:

            self.root.ids.status.text = "Selecione uma imagem primeiro"
            return

        imagem = Image.open(self.caminho)

        buffer = BytesIO()

        imagem.save(buffer, format="PNG")

        base64_img = base64.b64encode(buffer.getvalue()).decode()

        self.html = f"""<!DOCTYPE html>
<html>
<body>
<img src="data:image/png;base64,{base64_img}">
</body>
</html>"""

        self.root.ids.status.text = "Convertido com sucesso"

    def copiar(self):

        if not self.html:

            self.root.ids.status.text = "Nada para copiar"
            return

        Clipboard.copy(self.html)

        self.root.ids.status.text = "HTML copiado!"


AppPrincipal().run()
