# PMCL App（C# / Windows Forms）

这是一个使用 C#（微软语言）开发的 Minecraft 桌面启动器。

## 当前能力

- 启动游戏（兼容旧 `start_game.bat`）
- 多账户管理（offline / microsoft / yggdrasil）
- 第三方账户登录（例如 LittleSkin，基于 Yggdrasil）
- 多配置管理（版本、游戏目录、Java 路径、内存）
- 下载 Minecraft 最新正式版到程序目录下 `.minecraft`
- 启动历史记录与配置导出
- GitHub Actions 自动编译

## 项目结构

- `PMCL.sln`：Visual Studio 解决方案
- `src/PMCL.App/PMCL.App.csproj`：WinForms 项目文件
- `src/PMCL.App/Program.cs`：程序入口
- `src/PMCL.App/MainForm.cs`：主窗口与业务逻辑
- `src/PMCL.App/LauncherConfig.cs`：配置模型与存储
- `src/PMCL.App/OnlineServices.cs`：版本下载与第三方登录服务

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

工作流：`/.github/workflows/build-windows.yml`

- 在 `push / pull_request` 自动执行 `restore/build/publish`
- 上传 Artifact：`PMCL-App-win-x64`
