import qrcode
from pathlib import Path
import uuid


def gerar_qrcode(valor: float):

    codigo = f"""
LOJA FASHION
PIX DEMONSTRAÇÃO

VALOR:{valor:.2f}

TRANSACAO:{uuid.uuid4()}
"""

    pasta = Path("static/img/pix")
    pasta.mkdir(parents=True, exist_ok=True)

    caminho = pasta / "pix_atual.png"

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )

    qr.add_data(codigo)
    qr.make(fit=True)

    imagem = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    imagem.save(caminho)

    return "/static/img/pix/pix_atual.png"