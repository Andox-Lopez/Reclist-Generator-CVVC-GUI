# Reclist Generator for UTAU CVVC

A cross-platform GUI application for generating CVVC reclists for UTAU voicebanks.

## 📖 Introduction

This is a GUI-enhanced version of the original Reclist Generator for UTAU CVVC, which helps UTAU voicebank creators generate custom recording lists (reclists) quickly and efficiently.

## 👨‍💻 Original Author

- [**sdercolin**](https://github.com/sdercolin)
- **GitHub Repository**: [https://github.com/sdercolin/reclist-gen-cvvc/](https://github.com/sdercolin/reclist-gen-cvvc/)

## ✨ Features

- **Graphical User Interface**: Easy-to-use GUI for configuring all settings
- **Customizable Output**: Configure various parameters for your reclist
- **Multi-language Support**: Supports both English and Chinese
- **OTO Generation**: Automatically generates OTO settings
- **Real-time Configuration Saving**: Automatically saves your settings
- **Open Source**: Based on the original open-source project

## 🚀 Quick Start

### For Windows Users

1. Download the latest `reclist-gen.exe` from the releases page
2. Run the executable file
3. Configure your settings in the GUI
4. Click "Start Generation" to generate your reclist

## 🛠️ Installation from Source

If you prefer to run from source:

1. Clone or download this repository
2. Ensure you have Python 3.8 or higher installed
3. Run the GUI application:
   ```bash
   python reclist-gen-gui.py
   ```

## 📋 Usage

1. **Path Settings**:
   - Select your presamp.ini file
   - Set the output paths for your reclist and OTO files

2. **Reclist Settings**:
   - Configure the length per line
   - Choose whether to include all CV heads
   - Choose whether to include all VV connections
   - Set other formatting options

3. **OTO Settings**:
   - Configure the maximum number of same CVs
   - Set the maximum number of same VCs
   - Adjust preset blank and BPM settings
   - Choose whether to divide VCCV

4. **Generate**:
   - Click "Start Generation" to generate your reclist and OTO files
   - The application will show a success message when generation is complete

## 🔧 Configuration Options

### RECLIST Section
- `input_path`: Path to your presamp.ini file
- `reclist_output_path`: Output path for your reclist.txt file
- `length`: Length of each line in the reclist
- `include_CV_head`: Whether to include all CV heads
- `include_VV`: Whether to include all VV connections
- `use_underbar`: Whether to use underbars in the output
- `use_planb`: Whether to use PlanB formatting

### OTOSET Section
- `oto_output_path`: Output path for your oto.ini file
- `oto_max_of_same_cv`: Maximum number of same CVs
- `oto_max_of_same_vc`: Maximum number of same VCs
- `oto_preset_blank`: Preset blank value
- `oto_bpm`: BPM value
- `oto_devide_vccv`: Whether to divide VCCV

## 📁 Project Structure

```
reclist-gen-cvvc/
├── lang/                  # Language files
│   ├── en.json           # English translations
│   └── zh.json           # Chinese translations
├── presamp.ini           # Default presamp file
├── readme.txt            # Original readme file
├── reclist-gen-cvvc.ini  # Configuration file
├── reclist-gen-cvvc.py   # Core generation script
└── reclist-gen-gui.py    # GUI application
```

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute to this project, please:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Special thanks to **sdercolin** for creating the original reclist-gen-cvvc
- This project is based on the original repository: [https://github.com/sdercolin/reclist-gen-cvvc/](https://github.com/sdercolin/reclist-gen-cvvc/)

## 📞 Support

If you encounter any issues or have questions:

1. Check the original repository's issues page
2. Create a new issue in this repository
3. Contact the maintainers

## 📱 Contact

For any inquiries, please contact the maintainers of this repository.

---

**Based on the original work by sdercolin: [https://github.com/sdercolin/reclist-gen-cvvc/](https://github.com/sdercolin/reclist-gen-cvvc/)**
