"""
Core game launcher functionality.
Handles game launching and validation.
"""

import os
import subprocess
from pathlib import Path
from typing import Tuple, Optional

from ..config.constants import MIN_MEMORY_MB


class GameLauncher:
    """Handles Minecraft game launching logic."""

    def __init__(self, work_dir: str = "."):
        self.work_dir = Path(work_dir)
        self.start_script = self.work_dir / "start_game.bat"

    def validate_launch_params(
        self, username: str, maxmb: str, version: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate launch parameters before starting the game.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for empty values
        if not username or not maxmb or not version:
            return False, "请填完信息"
        
        # Check if maxmb is numeric
        if not maxmb.isnumeric():
            return False, "最大内存必须是数字！"
        
        # Check minimum memory requirement
        if int(maxmb) < MIN_MEMORY_MB:
            return False, f"内存设置必须要{MIN_MEMORY_MB}mb以上！"
        
        # Check unsupported versions
        if version == "1.12.2 Forge":
            return False, "启动失败！版本不支持！"
        
        return True, None

    def launch_game(self) -> bool:
        """
        Launch the game using start_game.bat.
        
        Returns:
            True if launch was successful, False otherwise.
        """
        try:
            if not self.start_script.exists():
                raise FileNotFoundError(f"Start script not found: {self.start_script}")
            
            # Use subprocess instead of os.startfile for better error handling
            subprocess.Popen(
                str(self.start_script),
                cwd=str(self.work_dir),
                shell=True
            )
            return True
        except Exception as e:
            # Log error here if logging is configured
            return False

    def launch_vape_lite(self) -> bool:
        """
        Launch Vape Lite patcher.
        
        Returns:
            True if launch was successful, False otherwise.
        """
        try:
            fix_script = self.work_dir / "fix.bat"
            patcher_exe = self.work_dir / "Kangaroo Patcher.exe"
            vape_exe = self.work_dir / "Vape_Lite.exe"
            
            if not fix_script.exists():
                raise FileNotFoundError("fix.bat not found")
            
            if not patcher_exe.exists():
                raise FileNotFoundError("Kangaroo Patcher.exe not found")
            
            # Run fix.bat first
            subprocess.run(str(fix_script), cwd=str(self.work_dir), shell=True, check=True)
            
            # Run patcher
            subprocess.Popen(
                f'"{patcher_exe}" Vape_Lite.exe',
                cwd=str(self.work_dir),
                shell=True
            )
            return True
        except Exception as e:
            return False
