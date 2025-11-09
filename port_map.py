"""
Windows Port Mapping GUI Tool
Map remote port to local port
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import re
import sys


class PortMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Port Mapper")
        self.root.geometry("650x600")
        self.root.resizable(True, True)  # 允许调整大小
        self.root.minsize(600, 550)  # 设置最小尺寸
        
        # 设置DPI感知以改善字体渲染
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass
        
        # 设置背景颜色
        self.root.configure(bg="#f5f6fa")
        
        # 设置图标和样式
        self.setup_ui()
        
        # 当前映射状态
        self.is_mapped = False
        self.current_remote_ip = None
        self.current_remote_port = None
        self.current_local_port = None
        
        # 启动时检查现有映射
        self.check_existing_mapping()
    
    def setup_ui(self):
        """Setup user interface"""
        # 顶部栏
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=90)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        # 标题
        title_container = tk.Frame(header_frame, bg="#2c3e50")
        title_container.pack(expand=True)
        
        icon_label = tk.Label(title_container, text="🔗", 
                             font=("Segoe UI Emoji", 32),
                             bg="#2c3e50", fg="#ffffff")
        icon_label.pack(side=tk.LEFT, padx=(0, 15))
        
        title_frame = tk.Frame(title_container, bg="#2c3e50")
        title_frame.pack(side=tk.LEFT)
        
        title_label = tk.Label(title_frame, text="Port Mapper", 
                              font=("Microsoft YaHei", 20, "bold"),
                              bg="#2c3e50", fg="#ffffff")
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(title_frame, text="Windows Port Forwarding Tool", 
                                 font=("Microsoft YaHei", 11),
                                 bg="#2c3e50", fg="#bdc3c7")
        subtitle_label.pack(anchor=tk.W)
        
        # 主内容区域
        content_frame = tk.Frame(self.root, bg="#f5f6fa")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=35, pady=30)
        
        # 信息提示卡片
        info_card = tk.Frame(content_frame, bg="#3498db", relief=tk.FLAT, bd=0)
        info_card.pack(fill=tk.X, pady=(0, 25))
        
        info_inner = tk.Frame(info_card, bg="#3498db")
        info_inner.pack(fill=tk.X, padx=20, pady=18)
        
        info_icon = tk.Label(info_inner, text="ℹ️", 
                            font=("Segoe UI Emoji", 18),
                            bg="#3498db", fg="#ffffff")
        info_icon.pack(side=tk.LEFT, padx=(0, 12))
        
        info_text = tk.Label(info_inner, 
                            text="Mapping: Remote IP:Port → Local Port", 
                            font=("Microsoft YaHei", 12, "bold"),
                            bg="#3498db", fg="#ffffff")
        info_text.pack(side=tk.LEFT)
        
        # 配置卡片
        config_card = tk.Frame(content_frame, bg="#ffffff", relief=tk.FLAT, bd=0)
        config_card.pack(fill=tk.X, pady=(0, 25))
        
        shadow_frame = tk.Frame(content_frame, bg="#dfe6e9", relief=tk.FLAT)
        shadow_frame.place(in_=config_card, x=3, y=3, relwidth=1, relheight=1)
        config_card.lift()
        
        config_inner = tk.Frame(config_card, bg="#ffffff")
        config_inner.pack(fill=tk.X, padx=30, pady=25)
        
        # 远程IP地址
        ip_frame = tk.Frame(config_inner, bg="#ffffff")
        ip_frame.pack(fill=tk.X, pady=(0, 18))
        
        ip_label_frame = tk.Frame(ip_frame, bg="#ffffff")
        ip_label_frame.pack(fill=tk.X, pady=(0, 8))
        
        ip_icon = tk.Label(ip_label_frame, text="🌐", 
                          font=("Segoe UI Emoji", 14),
                          bg="#ffffff")
        ip_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        ip_label = tk.Label(ip_label_frame, text="Remote IP Address", 
                           font=("Microsoft YaHei", 11, "bold"),
                           bg="#ffffff", fg="#2c3e50")
        ip_label.pack(side=tk.LEFT)
        
        self.remote_ip_entry = tk.Entry(ip_frame, 
                                        font=("Microsoft YaHei", 11),
                                        relief=tk.FLAT, 
                                        bg="#ecf0f1",
                                        fg="#2c3e50",
                                        insertbackground="#3498db")
        self.remote_ip_entry.pack(fill=tk.X, ipady=10, ipadx=12)
        self.remote_ip_entry.insert(0, "192.168.1.100")
        self.remote_ip_entry.bind("<FocusIn>", lambda e: self.on_entry_focus(e, True))
        self.remote_ip_entry.bind("<FocusOut>", lambda e: self.on_entry_focus(e, False))
        
        # 远程端口
        remote_port_frame = tk.Frame(config_inner, bg="#ffffff")
        remote_port_frame.pack(fill=tk.X, pady=(0, 18))
        
        remote_port_label_frame = tk.Frame(remote_port_frame, bg="#ffffff")
        remote_port_label_frame.pack(fill=tk.X, pady=(0, 8))
        
        remote_port_icon = tk.Label(remote_port_label_frame, text="🔌", 
                                    font=("Segoe UI Emoji", 14),
                                    bg="#ffffff")
        remote_port_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        remote_port_label = tk.Label(remote_port_label_frame, text="Remote Port", 
                                     font=("Microsoft YaHei", 11, "bold"),
                                     bg="#ffffff", fg="#2c3e50")
        remote_port_label.pack(side=tk.LEFT)
        
        self.remote_port_entry = tk.Entry(remote_port_frame, 
                                          font=("Microsoft YaHei", 11),
                                          relief=tk.FLAT,
                                          bg="#ecf0f1",
                                          fg="#2c3e50",
                                          insertbackground="#3498db")
        self.remote_port_entry.pack(fill=tk.X, ipady=10, ipadx=12)
        self.remote_port_entry.insert(0, "2222")
        self.remote_port_entry.bind("<FocusIn>", lambda e: self.on_entry_focus(e, True))
        self.remote_port_entry.bind("<FocusOut>", lambda e: self.on_entry_focus(e, False))
        
        # 本地端口
        local_port_frame = tk.Frame(config_inner, bg="#ffffff")
        local_port_frame.pack(fill=tk.X, pady=(0, 8))
        
        local_port_label_frame = tk.Frame(local_port_frame, bg="#ffffff")
        local_port_label_frame.pack(fill=tk.X, pady=(0, 8))
        
        local_port_icon = tk.Label(local_port_label_frame, text="🏠", 
                                   font=("Segoe UI Emoji", 14),
                                   bg="#ffffff")
        local_port_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        local_port_label = tk.Label(local_port_label_frame, text="Local Port", 
                                    font=("Microsoft YaHei", 11, "bold"),
                                    bg="#ffffff", fg="#2c3e50")
        local_port_label.pack(side=tk.LEFT)
        
        self.local_port_entry = tk.Entry(local_port_frame, 
                                         font=("Microsoft YaHei", 11),
                                         relief=tk.FLAT,
                                         bg="#ecf0f1",
                                         fg="#2c3e50",
                                         insertbackground="#3498db")
        self.local_port_entry.pack(fill=tk.X, ipady=10, ipadx=12)
        self.local_port_entry.insert(0, "22")
        self.local_port_entry.bind("<FocusIn>", lambda e: self.on_entry_focus(e, True))
        self.local_port_entry.bind("<FocusOut>", lambda e: self.on_entry_focus(e, False))
        
        # 按钮区域
        button_container = tk.Frame(content_frame, bg="#f5f6fa")
        button_container.pack(fill=tk.X, pady=(0, 25))
        
        self.map_button = self.create_button(
            button_container, "▶ Create Mapping", "#27ae60", self.create_mapping
        )
        self.map_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        self.unmap_button = self.create_button(
            button_container, "⏹ Delete Mapping", "#e74c3c", self.delete_mapping
        )
        self.unmap_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(10, 10))
        
        self.refresh_button = self.create_button(
            button_container, "🔄 Refresh", "#95a5a6", self.check_existing_mapping
        )
        self.refresh_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(10, 0))
        
        # 状态卡片
        status_card = tk.Frame(content_frame, bg="#ffffff", relief=tk.FLAT)
        status_card.pack(fill=tk.X, pady=(0, 20))
        
        status_inner = tk.Frame(status_card, bg="#ffffff")
        status_inner.pack(fill=tk.X, padx=25, pady=18)
        
        status_icon_label = tk.Label(status_inner, text="📊", 
                                     font=("Segoe UI Emoji", 16),
                                     bg="#ffffff")
        status_icon_label.pack(side=tk.LEFT, padx=(0, 12))
        
        self.status_label = tk.Label(status_inner, text="Status: Not Mapped", 
                                    font=("Microsoft YaHei", 12, "bold"),
                                    bg="#ffffff", fg="#95a5a6")
        self.status_label.pack(side=tk.LEFT)
        
        # 日志卡片
        log_card = tk.Frame(content_frame, bg="#ffffff", relief=tk.FLAT)
        log_card.pack(fill=tk.BOTH, expand=True)
        
        log_header = tk.Frame(log_card, bg="#ecf0f1")
        log_header.pack(fill=tk.X)
        
        log_title = tk.Label(log_header, text="📝 Log Messages", 
                            font=("Microsoft YaHei", 10, "bold"),
                            bg="#ecf0f1", fg="#7f8c8d")
        log_title.pack(anchor=tk.W, padx=18, pady=10)
        
        log_content = tk.Frame(log_card, bg="#ffffff")
        log_content.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 18))
        
        self.log_text = tk.Text(log_content, height=6, 
                               font=("Microsoft YaHei", 10), 
                               wrap=tk.WORD,
                               bg="#fafafa", 
                               fg="#2c3e50",
                               relief=tk.FLAT, 
                               borderwidth=0,
                               padx=12, 
                               pady=12)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(log_content, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        self.log_text.config(state=tk.DISABLED)
        
        # 底部提示
        footer_frame = tk.Frame(self.root, bg="#34495e", height=38)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        tip_label = tk.Label(footer_frame, 
                            text="⚠ Requires Administrator Privileges  |  Windows Port Forwarding Tool  |  v1.1", 
                            font=("Microsoft YaHei", 9),
                            bg="#34495e", fg="#bdc3c7")
        tip_label.pack(expand=True)
    
    def create_button(self, parent, text, color, command):
        """创建自定义样式的按钮"""
        button = tk.Button(parent, 
                          text=text,
                          font=("Microsoft YaHei", 11, "bold"),
                          bg=color,
                          fg="#ffffff",
                          relief=tk.FLAT,
                          cursor="hand2",
                          command=command,
                          padx=20,
                          pady=14,
                          activebackground=self.darken_color(color),
                          activeforeground="#ffffff",
                          borderwidth=0)
        
        # 悬停效果
        button.bind("<Enter>", lambda e: button.config(bg=self.lighten_color(color)))
        button.bind("<Leave>", lambda e: button.config(bg=color))
        
        return button
    
    def lighten_color(self, color):
        """使颜色变亮"""
        color_map = {
            "#27ae60": "#2ecc71",
            "#e74c3c": "#ec7063",
            "#95a5a6": "#aab7b8"
        }
        return color_map.get(color, color)
    
    def darken_color(self, color):
        """使颜色变暗"""
        color_map = {
            "#27ae60": "#229954",
            "#e74c3c": "#c0392b",
            "#95a5a6": "#7f8c8d"
        }
        return color_map.get(color, color)
    
    def on_entry_focus(self, event, is_focus):
        """输入框焦点效果"""
        if is_focus:
            event.widget.config(bg="#ffffff", relief=tk.SOLID, borderwidth=2)
        else:
            event.widget.config(bg="#ecf0f1", relief=tk.FLAT, borderwidth=0)
    
    def log(self, message):
        """添加日志信息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def check_admin(self):
        """检查是否具有管理员权限"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    
    def validate_ip(self, ip):
        """验证IP地址格式"""
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(pattern, ip):
            parts = ip.split('.')
            return all(0 <= int(part) <= 255 for part in parts)
        return False
    
    def validate_port(self, port):
        """验证端口号"""
        try:
            port_num = int(port)
            return 1 <= port_num <= 65535
        except:
            return False
    
    def check_existing_mapping(self):
        """Check existing port mappings"""
        try:
            self.log("Checking existing mappings...")
            result = subprocess.run(
                ["netsh", "interface", "portproxy", "show", "all"],
                capture_output=True,
                text=True,
                encoding='gbk',
                errors='ignore'
            )
            
            if result.returncode == 0:
                output = result.stdout
                if output:
                    # Find connections forwarding to local port (connectaddress=127.0.0.1)
                    lines = output.split('\n')
                    for i, line in enumerate(lines):
                        if line and '127.0.0.1' in line:
                            # Try to parse mapping info
                            parts = line.split()
                            if len(parts) >= 4:
                                # parts[0]=listen address, parts[1]=listen port
                                # parts[2]=connect address, parts[3]=connect port
                                self.current_remote_ip = parts[0]
                                self.current_remote_port = parts[1]
                                self.current_local_port = parts[3]
                                self.is_mapped = True
                                self.status_label.config(
                                    text=f"Status: Mapped {self.current_remote_ip}:{self.current_remote_port} → Local:{self.current_local_port}",
                                    fg="#27ae60"
                                )
                                self.log(f"Found existing mapping: {self.current_remote_ip}:{self.current_remote_port} → Local:{self.current_local_port}")
                                return
                
                # No mapping found
                self.is_mapped = False
                self.status_label.config(text="Status: Not Mapped", fg="#95a5a6")
                self.log("No existing mapping found")
            else:
                error_msg = result.stderr if result.stderr else "Unknown error"
                self.log(f"Check failed: {error_msg}")
        except Exception as e:
            self.log(f"Error checking mapping: {str(e)}")
            # Set to not mapped state even on error
            self.is_mapped = False
            self.status_label.config(text="Status: Not Mapped", fg="#95a5a6")
    
    def create_mapping(self):
        """Create port mapping"""
        remote_ip = self.remote_ip_entry.get().strip()
        remote_port = self.remote_port_entry.get().strip()
        local_port = self.local_port_entry.get().strip()
        
        # Validate input
        if not remote_ip:
            messagebox.showerror("Error", "Please enter remote IP address")
            return
        
        if not remote_port:
            messagebox.showerror("Error", "Please enter remote port")
            return
        
        if not local_port:
            messagebox.showerror("Error", "Please enter local port")
            return
        
        if not self.validate_ip(remote_ip):
            messagebox.showerror("Error", "Invalid IP address format")
            return
        
        if not self.validate_port(remote_port):
            messagebox.showerror("Error", "Port number must be between 1-65535")
            return
        
        if not self.validate_port(local_port):
            messagebox.showerror("Error", "Local port must be between 1-65535")
            return
        
        # Check admin privileges
        if not self.check_admin():
            messagebox.showerror("Permission Denied", 
                               "This program requires administrator privileges\nPlease run as administrator")
            self.log("Error: Administrator privileges required")
            return
        
        # Delete existing mapping if any
        if self.is_mapped:
            self.log("Existing mapping detected, removing...")
            self.delete_mapping(silent=True)
        
        try:
            self.log(f"Creating mapping: {remote_ip}:{remote_port} → Local:{local_port}")
            
            # Use netsh to create port forwarding (remote → local)
            cmd = [
                "netsh", "interface", "portproxy", "add", "v4tov4",
                f"listenport={remote_port}",
                f"listenaddress={remote_ip}",
                f"connectport={local_port}",
                "connectaddress=127.0.0.1"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='gbk', errors='ignore')
            
            if result.returncode == 0:
                self.is_mapped = True
                self.current_remote_ip = remote_ip
                self.current_remote_port = remote_port
                self.current_local_port = local_port
                self.status_label.config(
                    text=f"Status: Mapped {remote_ip}:{remote_port} → Local:{local_port}",
                    fg="#27ae60"
                )
                self.log("Mapping created successfully!")
                messagebox.showinfo("Success", f"Port mapping created!\n{remote_ip}:{remote_port} → Local:{local_port}")
            else:
                error_msg = result.stderr if result.stderr else "Unknown error"
                self.log(f"Failed to create mapping: {error_msg}")
                messagebox.showerror("Error", f"Failed to create mapping:\n{error_msg}")
        
        except Exception as e:
            self.log(f"Error creating mapping: {str(e)}")
            messagebox.showerror("Error", f"Error creating mapping:\n{str(e)}")
    
    def delete_mapping(self, silent=False):
        """Delete port mapping"""
        # Check admin privileges
        if not self.check_admin():
            if not silent:
                messagebox.showerror("Permission Denied", 
                                   "This program requires administrator privileges\nPlease run as administrator")
            self.log("Error: Administrator privileges required")
            return
        
        try:
            self.log("Deleting port mapping...")
            
            # Need to know the original listen port and address
            if self.current_remote_ip and self.current_remote_port:
                cmd = [
                    "netsh", "interface", "portproxy", "delete", "v4tov4",
                    f"listenport={self.current_remote_port}",
                    f"listenaddress={self.current_remote_ip}"
                ]
            else:
                # If no specific info available
                self.log("Warning: Cannot determine mapping details")
                if not silent:
                    messagebox.showwarning("Warning", "Cannot determine mapping information, please delete manually")
                return
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='gbk', errors='ignore')
            
            if result.returncode == 0:
                self.is_mapped = False
                self.current_remote_ip = None
                self.current_remote_port = None
                self.current_local_port = None
                self.status_label.config(text="Status: Not Mapped", fg="#95a5a6")
                self.log("Mapping deleted successfully!")
                if not silent:
                    messagebox.showinfo("Success", "Port mapping deleted")
            else:
                error_msg = result.stderr if result.stderr else "Unknown error"
                self.log(f"Failed to delete mapping: {error_msg}")
                if not silent:
                    messagebox.showerror("Error", f"Failed to delete mapping:\n{error_msg}")
        
        except Exception as e:
            self.log(f"Error deleting mapping: {str(e)}")
            if not silent:
                messagebox.showerror("Error", f"Error deleting mapping:\n{str(e)}")


def main():
    root = tk.Tk()
    app = PortMapApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
