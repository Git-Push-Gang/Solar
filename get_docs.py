import json

from docx import Document
import os

data = "./kareumstay"


# .docx 파일의 내용을 읽어오는 함수
def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)


# # 디렉토리 구조를 재귀적으로 탐색하여 사전 형태로 반환하는 함수
def get_full_directory_structure(directory):
    directory_structure = {}
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):

            # 하위 폴더에 대해서도 재귀적으로 탐색
            directory_structure[item] = get_full_directory_structure(item_path)

        else:
            # '.docx' 확장자를 제거하고 이름만 사용
            if item.endswith(".docx"):
                item_name = item.replace("_.docx", "")

                try:
                    # .docx 파일의 내용을 읽어서 JSON에 포함
                    content = read_docx(item_path)
                    directory_structure[item_name] = content
                except Exception as e:
                    directory_structure[item_name] = f"Error: {str(e)}"
            else:
                # 다른 파일의 경우 이름만 기록
                item_name = os.path.splitext(item)[0]
                directory_structure[item_name] = None
    return directory_structure



full_directory_structure = get_full_directory_structure(data)

# 출력용
# full_directory_structure_json = json.dumps(
#     full_directory_structure, indent=4, ensure_ascii=False
# )
# print(full_directory_structure_json)
