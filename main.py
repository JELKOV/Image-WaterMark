import tkinter as tk
from tkinter import filedialog, ttk, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Application")  # 프로그램 창 제목 설정
        self.root.geometry("600x800")  # 창 크기 설정

        # ttk 스타일 설정
        style = ttk.Style()
        style.theme_use('clam')  # 'clam' 테마 적용

        # 초기 변수 설정
        self.current_image = None  # 현재 업로드된 이미지를 저장할 변수
        self.original_image = None  # 원본 이미지를 저장할 변수
        self.watermark_text = tk.StringVar()  # 워터마크 텍스트를 저장할 변수
        self.watermark_position = None  # 워터마크 좌표
        self.watermark_opacity = tk.DoubleVar(value=1.0)  # 워터마크 투명도 초기값 설정
        self.watermark_color = "#FFFFFF"  # 워터마크 텍스트 색상 (기본값: 흰색)
        self.watermark_font_size = tk.IntVar(value=30)  # 워터마크 글자 크기 초기값 설정

        self.setup_ui()  # UI 구성

    def setup_ui(self):
        # 상단 프레임 (이미지 업로드 및 워터마크 입력 관련 위젯)
        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=10)

        # 이미지 업로드 버튼
        ttk.Button(top_frame, text="Upload Image", command=self.upload_image).grid(row=0, column=0, padx=5)

        # 워터마크 텍스트 입력 필드
        ttk.Entry(top_frame, textvariable=self.watermark_text, width=30).grid(row=0, column=1, padx=5)

        # 워터마크 적용 버튼
        ttk.Button(top_frame, text="Apply Watermark", command=self.apply_watermark).grid(row=0, column=2, padx=5)

        # 워터마크 색상 선택 버튼
        ttk.Button(top_frame, text="Select Color", command=self.choose_color).grid(row=0, column=3, padx=5)

        # 워터마크 위치 선택 안내
        position_label = ttk.Label(self.root, text="Click on the image to set watermark position.")
        position_label.pack(pady=5)

        # 워터마크 투명도 설정 슬라이더
        opacity_label = ttk.Label(self.root, text="Opacity:")
        opacity_label.pack(pady=5)
        opacity_slider = ttk.Scale(self.root, variable=self.watermark_opacity, from_=0.1, to=1.0, orient=tk.HORIZONTAL)
        opacity_slider.pack(pady=5)

        # 워터마크 글자 크기 설정 슬라이더
        font_size_label = ttk.Label(self.root, text="Font Size:")
        font_size_label.pack(pady=5)
        font_size_slider = ttk.Scale(self.root, variable=self.watermark_font_size, from_=10, to=100, orient=tk.HORIZONTAL)
        font_size_slider.pack(pady=5)

        # 이미지 미리보기용 캔버스
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="gray")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.set_position)  # 클릭 이벤트 연결

        # 클릭 좌표 표시 라벨
        self.position_label = ttk.Label(self.root, text="Click position: (x, y)")
        self.position_label.pack(pady=5)

        # Reset 버튼
        ttk.Button(self.root, text="Reset", command=self.reset_image).pack(pady=5)

        # 이미지 저장 버튼
        ttk.Button(self.root, text="Save Image", command=self.save_image).pack(pady=5)

    def set_position(self, event):
        # 마우스 클릭 이벤트로 워터마크 위치 설정
        self.watermark_position = (event.x, event.y)  # 캔버스 내 클릭 좌표 저장
        self.position_label.config(text=f"Click position: ({event.x}, {event.y})")  # 라벨에 좌표 표시
        print(f"Watermark position set to: {self.watermark_position}")

        # 캔버스에 클릭 표시 (원 추가)
        self.canvas.delete("position_marker")  # 기존 표시 삭제
        self.canvas.create_oval(
            event.x - 5, event.y - 5, event.x + 5, event.y + 5,
            outline="red", fill="red", tags="position_marker"
        )

    def upload_image(self):
        # 파일 다이얼로그를 열어 이미지를 선택하는 함수
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.original_image = Image.open(file_path).convert("RGBA")  # RGBA 모드로 변환 (투명도 지원)
            self.current_image = self.original_image.copy()  # 복사본 생성
            self.display_image(self.current_image)  # 이미지를 캔버스에 표시

    def display_image(self, img):
        # 이미지를 미리보기용으로 캔버스에 표시하는 함수
        img.thumbnail((400, 400))  # 이미지를 캔버스 크기에 맞게 축소
        tk_img = ImageTk.PhotoImage(img)  # Tkinter에서 사용할 이미지 형식으로 변환
        self.canvas.create_image(200, 200, image=tk_img)  # 캔버스 중앙에 이미지 배치
        self.canvas.image = tk_img  # 이미지 객체를 참조로 유지 (Garbage Collection 방지)

    def apply_watermark(self):
        # 업로드된 이미지에 워터마크를 추가하는 함수
        if self.current_image and self.watermark_text.get() and self.watermark_position:
            # 워터마크 텍스트와 폰트 설정
            text = self.watermark_text.get()
            font_size = self.watermark_font_size.get()  # 슬라이더에서 글자 크기 값 가져오기
            font = ImageFont.truetype("arial.ttf", font_size)
            draw = ImageDraw.Draw(self.current_image)

            # 투명도 적용 (텍스트와 배경 혼합)
            overlay = Image.new("RGBA", self.current_image.size, (255, 255, 255, 0))
            draw_overlay = ImageDraw.Draw(overlay)
            draw_overlay.text(self.watermark_position, text, font=font,
                              fill=self.watermark_color + f"{int(self.watermark_opacity.get() * 255):02x}")
            self.current_image = Image.alpha_composite(self.current_image, overlay)

            # 변경된 이미지를 미리보기로 표시
            self.display_image(self.current_image)

    def reset_image(self):
        # 원본 이미지로 되돌리는 함수
        if self.original_image:
            self.current_image = self.original_image.copy()  # 원본 복사
            self.watermark_position = None  # 위치 초기화
            self.display_image(self.current_image)  # 원본 이미지를 캔버스에 표시

    def choose_color(self):
        # 색상 선택 다이얼로그를 열어 사용자가 색상을 선택하도록 함
        color_code = colorchooser.askcolor(title="Choose Text Color")[1]
        if color_code:
            self.watermark_color = color_code  # 선택된 색상 저장

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
