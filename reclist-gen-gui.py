import tkinter as tk
from tkinter import ttk, filedialog, Menu
import configparser
import subprocess
import sys
import os
import webbrowser

import json

# 语言管理类
class LanguageManager:
    def __init__(self):
        self.current_language = "zh"
        self.languages = {
            "zh": "中文",
            "en": "English"
        }
        self.translations = {}
        self.lang_dir = "lang"
        # 确保语言目录存在
        if not os.path.exists(self.lang_dir):
            os.makedirs(self.lang_dir)
        # 加载所有语言的翻译
        self.load_all_translations()
    
    def load_all_translations(self):
        # 加载所有语言的翻译文件
        for lang_code in self.languages.keys():
            self.load_translation(lang_code)
    
    def load_translation(self, lang_code):
        # 从JSON文件加载翻译
        file_path = os.path.join(self.lang_dir, f"{lang_code}.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.translations[lang_code] = json.load(f)
        except FileNotFoundError:
            # 如果文件不存在，创建默认翻译
            self.translations[lang_code] = self.create_default_translation(lang_code)
            # 保存默认翻译到文件
            self.save_translation(lang_code)
        except json.JSONDecodeError:
            # 如果JSON文件格式错误，使用默认翻译
            self.translations[lang_code] = self.create_default_translation(lang_code)
    
    def create_default_translation(self, lang_code):
        # 创建默认翻译
        default_translation = {
            "title": "Reclist Generator",
            "path_settings": "路径设置" if lang_code == "zh" else "Path Settings",
            "input_file_path": "输入文件路径：" if lang_code == "zh" else "Input File Path:",
            "browse": "浏览" if lang_code == "zh" else "Browse",
            "reclist_output_path": "Reclist输出路径：" if lang_code == "zh" else "Reclist Output Path:",
            "oto_output_path": "OTO输出路径：" if lang_code == "zh" else "OTO Output Path:",
            "reclist_settings": "录音表设置" if lang_code == "zh" else "Reclist Settings",
            "length_per_line": "每行长度：" if lang_code == "zh" else "Length per line:",
            "include_cv_head": "生成所有起始音" if lang_code == "zh" else "Include all CV heads",
            "include_vv": "生成所有VV连接" if lang_code == "zh" else "Include all VV connections",
            "use_underbar": "使用下划线" if lang_code == "zh" else "Use underbar",
            "planb": "PlanB",
            "oto_settings": "OTO设置" if lang_code == "zh" else "OTO Settings",
            "max_same_cv": "相同CV最大数量：" if lang_code == "zh" else "Max same CV:",
            "max_same_vc": "相同VC最大数量：" if lang_code == "zh" else "Max same VC:",
            "preset_blank": "预设空白：" if lang_code == "zh" else "Preset blank:",
            "bpm": "BPM：" if lang_code == "zh" else "BPM:",
            "divide_vccv": "分割VCCV" if lang_code == "zh" else "Divide VCCV",
            "start_generation": "开始生成" if lang_code == "zh" else "Start Generation",
            "exit": "退出" if lang_code == "zh" else "Exit",
            "generation_success": "生成成功" if lang_code == "zh" else "Generation Success",
            "generation_failed": "生成失败" if lang_code == "zh" else "Generation Failed",
            "success_message": "Reclist和OTO文件已成功生成！" if lang_code == "zh" else "Reclist and OTO files have been successfully generated!",
            "error_message": "生成过程中出现错误：{}" if lang_code == "zh" else "Error during generation: {}",
            "unknown_error": "发生未知错误：{}" if lang_code == "zh" else "Unknown error occurred: {}",
            "menu_language": "语言" if lang_code == "zh" else "Language",
            "menu_help": "帮助" if lang_code == "zh" else "Help",
            "menu_readme": "查看README" if lang_code == "zh" else "View README",
            "menu_github": "开源地址" if lang_code == "zh" else "GitHub"
        }
        return default_translation
    
    def save_translation(self, lang_code):
        # 保存翻译到JSON文件
        file_path = os.path.join(self.lang_dir, f"{lang_code}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.translations[lang_code], f, ensure_ascii=False, indent=4)
    
    def set_language(self, lang):
        if lang in self.languages:
            self.current_language = lang
    
    def get(self, key, *args):
        # 确保当前语言的翻译已加载
        if self.current_language not in self.translations:
            self.load_translation(self.current_language)
        
        # 获取翻译
        translation = self.translations[self.current_language].get(key, key)
        if args:
            translation = translation.format(*args)
        return translation
    
    def get_available_languages(self):
        # 获取可用的语言列表
        return self.languages.copy()

class ReclistGeneratorGUI:
    def __init__(self, root):
        self.root = root
        
        # 初始化语言管理器
        self.lang_manager = LanguageManager()
        
        self.root.title(self.lang_manager.get("title"))
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        
        # 读取配置文件
        self.config = configparser.ConfigParser()
        self.config_file = "reclist-gen-cvvc.ini"
        self.load_config()
        
        # 创建菜单栏
        self.create_menu()
        
        # 添加窗口关闭事件处理
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建路径设置框架
        self.create_path_frame()
        
        # 创建录音表设置框架
        self.create_reclist_frame()
        
        # 创建OTO设置框架
        self.create_oto_frame()
        
        # 创建按钮框架
        self.create_button_frame()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file, encoding="utf-8")
        else:
            # 默认配置
            self.config["RECLIST"] = {
                "input_path": "./presamp.ini",
                "reclist_output_path": "Reclist.txt",
                "length": "8",
                "include_CV_head": "True",
                "include_VV": "True",
                "use_underbar": "True",
                "use_planb": "False"
            }
            self.config["OTOSET"] = {
                "oto_output_path": "oto.ini",
                "oto_max_of_same_cv": "1",
                "oto_max_of_same_vc": "1",
                "oto_preset_blank": "1250",
                "oto_bpm": "130",
                "oto_devide_vccv": "True"
            }
            self.save_config()
    
    def save_config(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            self.config.write(f)
    
    def create_path_frame(self):
        frame = ttk.LabelFrame(self.main_frame, text=self.lang_manager.get("path_settings"), padding="15")
        frame.pack(fill=tk.X, pady=(0, 15))
        
        # 输入文件路径
        ttk.Label(frame, text=self.lang_manager.get("input_file_path")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_path_var = tk.StringVar(value=self.config["RECLIST"]["input_path"])
        input_path_entry = ttk.Entry(frame, textvariable=self.input_path_var, width=30)
        input_path_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text=self.lang_manager.get("browse"), command=self.browse_input_path).grid(row=0, column=2, padx=5, pady=5)
        
        # Reclist输出路径
        ttk.Label(frame, text=self.lang_manager.get("reclist_output_path")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.reclist_output_var = tk.StringVar(value=self.config["RECLIST"]["reclist_output_path"])
        reclist_output_entry = ttk.Entry(frame, textvariable=self.reclist_output_var, width=30)
        reclist_output_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text=self.lang_manager.get("browse"), command=self.browse_reclist_output_path).grid(row=1, column=2, padx=5, pady=5)
        
        # OTO输出路径
        ttk.Label(frame, text=self.lang_manager.get("oto_output_path")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.oto_output_var = tk.StringVar(value=self.config["OTOSET"]["oto_output_path"])
        oto_output_entry = ttk.Entry(frame, textvariable=self.oto_output_var, width=30)
        oto_output_entry.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(frame, text=self.lang_manager.get("browse"), command=self.browse_oto_output_path).grid(row=2, column=2, padx=5, pady=5)
    
    def browse_input_path(self):
        filename = filedialog.askopenfilename(filetypes=[("INI Files", "*.ini"), ("All Files", "*.*")])
        if filename:
            self.input_path_var.set(filename)
    
    def browse_reclist_output_path(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filename:
            self.reclist_output_var.set(filename)
    
    def browse_oto_output_path(self):
        filename = filedialog.asksaveasfilename(defaultextension=".ini", filetypes=[("INI Files", "*.ini"), ("All Files", "*.*")])
        if filename:
            self.oto_output_var.set(filename)
    
    def create_reclist_frame(self):
        frame = ttk.LabelFrame(self.main_frame, text=self.lang_manager.get("reclist_settings"), padding="15")
        frame.pack(fill=tk.X, pady=(0, 15))
        
        # 每行长度
        ttk.Label(frame, text=self.lang_manager.get("length_per_line")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.length_var = tk.IntVar(value=int(self.config["RECLIST"]["length"]))
        length_spinbox = ttk.Spinbox(frame, from_=1, to=20, textvariable=self.length_var, width=5)
        length_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # 生成所有起始音
        self.include_cv_head_var = tk.BooleanVar(value=self.config["RECLIST"]["include_CV_head"] == "True")
        ttk.Checkbutton(frame, text=self.lang_manager.get("include_cv_head"), variable=self.include_cv_head_var).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # 生成所有VV连接
        self.include_vv_var = tk.BooleanVar(value=self.config["RECLIST"]["include_VV"] == "True")
        ttk.Checkbutton(frame, text=self.lang_manager.get("include_vv"), variable=self.include_vv_var).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # 使用下划线
        self.use_underbar_var = tk.BooleanVar(value=self.config["RECLIST"]["use_underbar"] == "True")
        ttk.Checkbutton(frame, text=self.lang_manager.get("use_underbar"), variable=self.use_underbar_var).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # PlanB
        self.use_planb_var = tk.BooleanVar(value=self.config["RECLIST"]["use_planb"] == "True")
        ttk.Checkbutton(frame, text=self.lang_manager.get("planb"), variable=self.use_planb_var).grid(row=2, column=1, sticky=tk.W, pady=5)
    
    def create_oto_frame(self):
        frame = ttk.LabelFrame(self.main_frame, text=self.lang_manager.get("oto_settings"), padding="15")
        frame.pack(fill=tk.X, pady=(0, 15))
        
        # 相同CV最大数量
        ttk.Label(frame, text=self.lang_manager.get("max_same_cv")).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.oto_max_cv_var = tk.IntVar(value=int(self.config["OTOSET"]["oto_max_of_same_cv"]))
        oto_max_cv_spinbox = ttk.Spinbox(frame, from_=1, to=10, textvariable=self.oto_max_cv_var, width=5)
        oto_max_cv_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # 相同VC最大数量
        ttk.Label(frame, text=self.lang_manager.get("max_same_vc")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.oto_max_vc_var = tk.IntVar(value=int(self.config["OTOSET"]["oto_max_of_same_vc"]))
        oto_max_vc_spinbox = ttk.Spinbox(frame, from_=1, to=10, textvariable=self.oto_max_vc_var, width=5)
        oto_max_vc_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # 预设空白
        ttk.Label(frame, text=self.lang_manager.get("preset_blank")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.oto_preset_blank_var = tk.IntVar(value=int(self.config["OTOSET"]["oto_preset_blank"]))
        oto_preset_blank_spinbox = ttk.Spinbox(frame, from_=0, to=5000, textvariable=self.oto_preset_blank_var, width=7)
        oto_preset_blank_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # BPM
        ttk.Label(frame, text=self.lang_manager.get("bpm")).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.oto_bpm_var = tk.IntVar(value=int(self.config["OTOSET"]["oto_bpm"]))
        oto_bpm_spinbox = ttk.Spinbox(frame, from_=60, to=200, textvariable=self.oto_bpm_var, width=5)
        oto_bpm_spinbox.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        # 使用下划线
        self.oto_devide_vccv_var = tk.BooleanVar(value=self.config["OTOSET"]["oto_devide_vccv"] == "True")
        ttk.Checkbutton(frame, text=self.lang_manager.get("divide_vccv"), variable=self.oto_devide_vccv_var).grid(row=4, column=0, sticky=tk.W, pady=5)
    
    def create_button_frame(self):
        frame = ttk.Frame(self.main_frame)
        frame.pack(fill=tk.X, pady=(10, 0))
        
        # 开始生成按钮
        start_button = ttk.Button(frame, text=self.lang_manager.get("start_generation"), command=self.start_generation)
        start_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 退出按钮
        exit_button = ttk.Button(frame, text=self.lang_manager.get("exit"), command=self.on_exit)
        exit_button.pack(side=tk.LEFT, padx=(0, 5))
    
    def start_generation(self):
        # 保存配置
        self.config["RECLIST"]["input_path"] = self.input_path_var.get()
        self.config["RECLIST"]["reclist_output_path"] = self.reclist_output_var.get()
        self.config["RECLIST"]["length"] = str(self.length_var.get())
        self.config["RECLIST"]["include_CV_head"] = str(self.include_cv_head_var.get())
        self.config["RECLIST"]["include_VV"] = str(self.include_vv_var.get())
        self.config["RECLIST"]["use_underbar"] = str(self.use_underbar_var.get())
        self.config["RECLIST"]["use_planb"] = str(self.use_planb_var.get())
        
        self.config["OTOSET"]["oto_output_path"] = self.oto_output_var.get()
        self.config["OTOSET"]["oto_max_of_same_cv"] = str(self.oto_max_cv_var.get())
        self.config["OTOSET"]["oto_max_of_same_vc"] = str(self.oto_max_vc_var.get())
        self.config["OTOSET"]["oto_preset_blank"] = str(self.oto_preset_blank_var.get())
        self.config["OTOSET"]["oto_bpm"] = str(self.oto_bpm_var.get())
        self.config["OTOSET"]["oto_devide_vccv"] = str(self.oto_devide_vccv_var.get())
        
        self.save_config()
        
        # 运行生成脚本
        try:
            subprocess.run([sys.executable, "reclist-gen-cvvc.py"], check=True, cwd=os.getcwd())
            # 显示生成成功消息
            self.show_info(self.lang_manager.get("generation_success"), self.lang_manager.get("success_message"))
        except subprocess.CalledProcessError as e:
            self.show_error(self.lang_manager.get("generation_failed"), self.lang_manager.get("error_message", e))
        except Exception as e:
            self.show_error(self.lang_manager.get("generation_failed"), self.lang_manager.get("unknown_error", e))
    
    def create_menu(self):
        # 创建菜单栏
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # 创建语言菜单
        language_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang_manager.get("menu_language"), menu=language_menu)
        
        # 添加语言选项
        for lang_code, lang_name in self.lang_manager.languages.items():
            language_menu.add_radiobutton(
                label=lang_name,
                command=lambda code=lang_code: self.change_language(code)
            )
        
        # 创建帮助菜单
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang_manager.get("menu_help"), menu=help_menu)
        
        # 添加查看README菜单项
        help_menu.add_command(
            label=self.lang_manager.get("menu_readme"),
            command=self.open_readme
        )
        
        # 添加开源地址菜单项
        help_menu.add_command(
            label=self.lang_manager.get("menu_github"),
            command=self.open_github
        )
    
    def change_language(self, lang_code):
        # 切换语言
        self.lang_manager.set_language(lang_code)
        # 更新标题
        self.root.title(self.lang_manager.get("title"))
        # 重新创建所有框架
        self.main_frame.destroy()
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.create_path_frame()
        self.create_reclist_frame()
        self.create_oto_frame()
        self.create_button_frame()
        # 重新创建菜单栏
        self.create_menu()
    
    def show_info(self, title, message):
        info_window = tk.Toplevel(self.root)
        info_window.title(title)
        info_window.geometry("300x150")
        info_window.resizable(False, False)
        
        # 计算居中位置
        self.root.update_idletasks()  # 确保获取最新的窗口大小
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        
        info_width = 300
        info_height = 150
        info_x = root_x + (root_width - info_width) // 2
        info_y = root_y + (root_height - info_height) // 2
        
        # 设置位置并显示
        info_window.geometry(f"{info_width}x{info_height}+{info_x}+{info_y}")
        info_window.transient(self.root)
        info_window.grab_set()
        
        ttk.Label(info_window, text=message, wraplength=280, padding=20).pack(fill=tk.BOTH, expand=True)
        ttk.Button(info_window, text="确定", command=info_window.destroy).pack(pady=10)
        
        info_window.wait_window()
    
    def show_error(self, title, message):
        error_window = tk.Toplevel(self.root)
        error_window.title(title)
        error_window.geometry("400x200")
        error_window.resizable(False, False)
        
        # 计算居中位置
        self.root.update_idletasks()  # 确保获取最新的窗口大小
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        
        error_width = 400
        error_height = 200
        error_x = root_x + (root_width - error_width) // 2
        error_y = root_y + (root_height - error_height) // 2
        
        # 设置位置并显示
        error_window.geometry(f"{error_width}x{error_height}+{error_x}+{error_y}")
        error_window.transient(self.root)
        error_window.grab_set()
        
        ttk.Label(error_window, text=message, wraplength=380, padding=20).pack(fill=tk.BOTH, expand=True)
        ttk.Button(error_window, text="确定", command=error_window.destroy).pack(pady=10)
        
        error_window.wait_window()
    
    def open_readme(self):
        # 打开readme.txt文件
        readme_path = os.path.join(os.getcwd(), "readme.txt")
        if os.path.exists(readme_path):
            if sys.platform == "win32":
                os.startfile(readme_path)
            else:
                subprocess.run(["open", readme_path])
    
    def open_github(self):
        # 打开开源地址
        webbrowser.open("http://github.com/sdercolin/reclist-gen-cvvc/")
    
    def on_exit(self):
        # 保存配置
        self.config["RECLIST"]["input_path"] = self.input_path_var.get()
        self.config["RECLIST"]["reclist_output_path"] = self.reclist_output_var.get()
        self.config["RECLIST"]["length"] = str(self.length_var.get())
        self.config["RECLIST"]["include_CV_head"] = str(self.include_cv_head_var.get())
        self.config["RECLIST"]["include_VV"] = str(self.include_vv_var.get())
        self.config["RECLIST"]["use_underbar"] = str(self.use_underbar_var.get())
        self.config["RECLIST"]["use_planb"] = str(self.use_planb_var.get())
        
        self.config["OTOSET"]["oto_output_path"] = self.oto_output_var.get()
        self.config["OTOSET"]["oto_max_of_same_cv"] = str(self.oto_max_cv_var.get())
        self.config["OTOSET"]["oto_max_of_same_vc"] = str(self.oto_max_vc_var.get())
        self.config["OTOSET"]["oto_preset_blank"] = str(self.oto_preset_blank_var.get())
        self.config["OTOSET"]["oto_bpm"] = str(self.oto_bpm_var.get())
        self.config["OTOSET"]["oto_devide_vccv"] = str(self.oto_devide_vccv_var.get())
        
        self.save_config()
        # 退出程序
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ReclistGeneratorGUI(root)
    root.mainloop()