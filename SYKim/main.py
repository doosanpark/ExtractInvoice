import fitz
from PIL import Image
import pytesseract
from pytesseract import Output
import easyocr
import io
import os
import time


def ocr_pdf(filename):
    current_directory = os.getcwd()
    print("Current Directory:", current_directory)
    print(f'Start OCR {filename}')

    document = fitz.open(filename)  # PDF 파일 열기

    # 출력 이미지를 저장할 디렉터리 생성
    if not os.path.exists('rendered_images'):
        os.makedirs('rendered_images')

    # 문서의 각 페이지를 이미지로 렌더링
    for page_number, page in enumerate(document):
        # 페이지를 이미지로 렌더링, zoom_x, zoom_y는 확대 비율
        zoom_x = 2.0
        zoom_y = 2.0
        mat = fitz.Matrix(zoom_x, zoom_y)  # 변환 행렬 생성

        # 페이지를 이미지 객체로 변환
        pix = page.get_pixmap(matrix=mat, alpha=False)  # 배경을 흰색으로 설정(alpha=False)

        # 이미지 파일로 저장
        current_time = time.strftime('%Y%m%d_%H%M%S')
        directory_name = f'rendered_images/{os.path.splitext(filename)[0]}_{current_time}'
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        image_filename = f'{directory_name}/{page_number + 1}.png'
        pix.save(image_filename)
        print(f'Saved: {image_filename}')

        # 이미지를 PIL 이미지 객체로 변환
        image = Image.open(image_filename)

        # html 시도중
        exact_html = False
        use_easyocr = False

        if exact_html:
            hocr_data_bytes = pytesseract.image_to_string(image, lang='kor+eng',
                                                          config='--oem 1 -c tessedit_create_hocr=1',
                                                          output_type=Output.BYTES)
            # 결과를 HTML 파일로 저장
            with open('output.hocr', 'wb') as file:
                file.write(hocr_data_bytes)
        elif use_easyocr:
            # 한글과 영어 인식을 위한 리더 생성
            reader = easyocr.Reader(['ko', 'en'])

            # 이미지에서 텍스트 인식
            result = reader.readtext("sample.jpeg")

            # 결과 출력
            for (bbox, text, prob) in result:
                print(f"{text}")
                # print(f"Probability: {prob}")
        else:
            text = pytesseract.image_to_string(image, lang='kor+eng')

            # 결과 출력
            print(f'Page {page_number + 1}')
            print(f'--------------------------------------------------------')
            print(text)
            print(f'--------------------------------------------------------')
    # 문서 닫기
    document.close()


def ocr_image(filename):
    # 이미지를 PIL 이미지 객체로 변환
    image = Image.open(filename)

    # html 시도중
    exact_html = False

    if exact_html:
        hocr_data_bytes = pytesseract.image_to_string(image, lang='kor+eng',
                                                      config='--oem 1 -c tessedit_create_hocr=1',
                                                      output_type=Output.BYTES)
        # 결과를 HTML 파일로 저장
        with open('output.hocr', 'wb') as file:
            file.write(hocr_data_bytes)
    else:
        text = pytesseract.image_to_string(image, lang='kor+eng')

        # 결과 출력
        print(f'--------------------------------------------------------')
        print(text)
        print(f'--------------------------------------------------------')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ocr_pdf('sample2.pdf')
    # ocr_image('sample.jpeg')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
