# PMCL App（C# / Windows Forms）

你说得对：这是 **桌面 App**，不是网页。

本项目已将主源码迁移为微软语言 **C#**，并使用 **Windows Forms** 实现启动器 GUI。

## 主要功能

- 启动游戏（兼容旧 `start_game.bat`）
- 多账户管理（offline / microsoft）
- 多配置管理（版本、游戏目录、Java 路径、内存）
- 启动历史记录
- 导出配置 JSON

## 项目结构

- `PMCL.sln`：Visual Studio 解决方案
- `src/PMCL.App/PMCL.App.csproj`：WinForms 项目文件
- `src/PMCL.App/Program.cs`：程序入口
- `src/PMCL.App/MainForm.cs`：主窗口与业务逻辑
- `src/PMCL.App/LauncherConfig.cs`：配置模型与存储

## 运行方式（Windows）

### 使用 Visual Studio

1. 打开 `PMCL.sln`
2. 选择 `PMCL.App` 为启动项目
3. F5 运行

### 使用 .NET CLI

```powershell
dotnet run --project .\src\PMCL.App\PMCL.App.csproj
```

## 兼容说明

启动前会继续写入以下文件，保持与旧链路兼容：

- `username.txt`
- `maxmb.txt`
- `version.txt`


## GitHub Actions 自动编译

仓库已添加工作流：`/.github/workflows/build-windows.yml`，在 `push / pull_request` 时会自动：

1. `dotnet restore`
2. `dotnet build -c Release`
3. `dotnet publish` 生成 `win-x64` 构建产物
4. 上传 Artifact：`PMCL-App-win-x64`
