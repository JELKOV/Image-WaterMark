import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Application")  # 프로그램 창 제목 설정
        self.root.geometry("600x800")  # 창 크기 설정

        # 초기 변수 설정
        self.current_image = None  # 현재 업로드된 이미지를 저장할 변수
        self.watermark_text = tk.StringVar()  # 워터마크 텍스트를 저장할 변수
        self.watermark_position = tk.StringVar(value="Center")  # 워터마크 위치 초기값 설정
        self.watermark_opacity = tk.DoubleVar(value=1.0)  # 워터마크 투명도 초기값 설정

        self.setup_ui()  # UI 구성

    def setup_ui(self):
        # 상단 프레임 (이미지 업로드 및 워터마크 입력 관련 위젯)
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        # 이미지 업로드 버튼
        tk.Button(top_frame, text="Upload Image", command=self.upload_image).grid(row=0, column=0, padx=5)

        # 워터마크 텍스트 입력 필드
        tk.Entry(top_frame, textvariable=self.watermark_text, width=30).grid(row=0, column=1, padx=5)

        # 워터마크 적용 버튼
        tk.Button(top_frame, text="Apply Watermark", command=self.apply_watermark).grid(row=0, column=2, padx=5)

        # 워터마크 위치 선택 드롭다운 메뉴
        position_label = tk.Label(self.root, text="Position:")
        position_label.pack(pady=5)
        position_dropdown = ttk.Combobox(self.root, textvariable=self.watermark_position,
                                         values=["Top Left", "Center", "Bottom Right"])
        position_dropdown.pack(pady=5)

        # 워터마크 투명도 설정 슬라이더
        opacity_label = tk.Label(self.root, text="Opacity:")
        opacity_label.pack(pady=5)
        opacity_slider = tk.Scale(self.root, variable=self.watermark_opacity, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL)
        opacity_slider.pack(pady=5)

        # 이미지 미리보기용 캔버스
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="gray")
        self.canvas.pack(pady=10)

        # 이미지 저장 버튼
        tk.Button(self.root, text="Save Image", command=self.save_image).pack(pady=5)

    def upload_image(self):
        # 파일 다이얼로그를 열어 이미지를 선택하는 함수
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.current_image = Image.open(file_path)  # Pillow로 이미지 열기
            self.display_image(self.current_image)  # 이미지를 캔버스에 표시

    def display_image(self, img):
        # 이미지를 미리보기용으로 캔버스에 표시하는 함수
        img.thumbnail((400, 400))  # 이미지를 캔버스 크기에 맞게 축소
        tk_img = ImageTk.PhotoImage(img)  # Tkinter에서 사용할 이미지 형식으로 변환
        self.canvas.create_image(200, 200, image=tk_img)  # 캔버스 중앙에 이미지 배치
        self.canvas.image = tk_img  # 이미지 객체를 참조로 유지 (Garbage Collection 방지)

    def apply_watermark(self):
        # 업로드된 이미지에 워터마크를 추가하는 함수
        if self.current_image:
            draw = ImageDraw.Draw(self.current_image)  # 이미지를 그릴 수 있는 객체 생성
            text = self.watermark_text.get()  # 입력된 워터마크 텍스트 가져오기
            font = ImageFont.truetype("arial.ttf", 20)  # 워터마크에 사용할 폰트 설정

            # 워터마크 위치 계산
            width, height = self.current_image.size  # 이미지 크기 가져오기
            position = {
                "Top Left": (10, 10),  # 좌상단
                "Center": (width // 2, height // 2),  # 중앙
                "Bottom Right": (width - 100, height - 30)  # 우하단
            }[self.watermark_position.get()]

            # 워터마크 텍스트 그리기
            draw.text(position, text, fill="white", font=font)
            self.display_image(self.current_image)  # 변경된 이미지를 캔버스에 다시 표시

    def save_image(self):
        # 워터마크가 추가된 이미지를 저장하는 함수
        if self.current_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
            if save_path:
                self.current_image.save(save_path)  # Pillow로 이미지 저장

# 프로그램 실행 코드
if __name__ == "__main__":
    root = tk.Tk()  # Tkinter 메인 윈도우 생성
    app = WatermarkApp(root)  # WatermarkApp 클래스의 인스턴스 생성
    root.mainloop()  # Tkinter 이벤트 루프 실행
