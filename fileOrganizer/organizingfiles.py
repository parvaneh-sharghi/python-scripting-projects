import os
import shutil

def organize_files_by_extension(source_folder):
    if not os.path.exists(source_folder):
        print(f"Error: Source folder '{source_folder}' does not exist.")
        return

    # لیست فایل‌های داخل فولدر
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        if os.path.isfile(file_path):
            # گرفتن پسوند فایل
            _, extension = os.path.splitext(filename)
            extension = extension.lower().strip('.')  # مثل 'jpg'

            if extension == '':
                extension = 'no_extension'

            # ساختن فولدر مقصد بر اساس پسوند
            destination_folder = os.path.join(source_folder, extension)
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            # انتقال فایل به فولدر جدید
            shutil.move(file_path, os.path.join(destination_folder, filename))
            print(f"Moved: {filename} -> {destination_folder}")

if __name__ == "__main__":
    # مسیر پوشه‌ای که میخوای فایل‌هاش مرتب بشه
    source_path = input().strip()
    organize_files_by_extension(source_path)