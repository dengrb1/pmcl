using System.Diagnostics;

namespace PMCL.App;

public sealed class MainForm : Form
{
    private LauncherConfig _config = new();

    private readonly ComboBox _launchProfile = new() { DropDownStyle = ComboBoxStyle.DropDownList, Dock = DockStyle.Fill };
    private readonly ComboBox _launchAccount = new() { DropDownStyle = ComboBoxStyle.DropDownList, Dock = DockStyle.Fill };
    private readonly TextBox _history = new() { Multiline = true, ScrollBars = ScrollBars.Vertical, ReadOnly = true, Dock = DockStyle.Fill };

    private readonly ListBox _profileList = new() { Dock = DockStyle.Fill };
    private readonly TextBox _pName = new();
    private readonly TextBox _pVersion = new();
    private readonly TextBox _pGameDir = new();
    private readonly TextBox _pJava = new();
    private readonly NumericUpDown _pMem = new() { Minimum = 900, Maximum = 16384, Value = 2048 };

    private readonly ListBox _accountList = new() { Dock = DockStyle.Fill };
    private readonly TextBox _aName = new();
    private readonly ComboBox _aType = new() { DropDownStyle = ComboBoxStyle.DropDownList };

    private readonly NumericUpDown _keepHistory = new() { Minimum = 10, Maximum = 500, Value = 100 };
    private readonly TextBox _yggdrasilServer = new() { Dock = DockStyle.Fill };
    private readonly TextBox _yggUsername = new() { Dock = DockStyle.Fill };
    private readonly TextBox _yggPassword = new() { Dock = DockStyle.Fill, UseSystemPasswordChar = true };

    private readonly Label _status = new() { Text = "就绪", Dock = DockStyle.Fill, AutoSize = true };

    public MainForm()
    {
        Text = "PMCL App (C# / Windows Forms)";
        Width = 1024;
        Height = 760;
        MinimumSize = new Size(900, 620);
        StartPosition = FormStartPosition.CenterScreen;

        _aType.Items.AddRange(new object[] { "offline", "microsoft", "yggdrasil" });
        _aType.SelectedIndex = 0;

        BuildUI();
        LoadConfig();
    }

    private void BuildUI()
    {
        var root = new TableLayoutPanel { Dock = DockStyle.Fill, RowCount = 2 };
        root.RowStyles.Add(new RowStyle(SizeType.Percent, 100));
        root.RowStyles.Add(new RowStyle(SizeType.Absolute, 28));

        var tabs = new TabControl { Dock = DockStyle.Fill };
        tabs.TabPages.Add(CreateLaunchTab());
        tabs.TabPages.Add(CreateProfileTab());
        tabs.TabPages.Add(CreateAccountTab());
        tabs.TabPages.Add(CreateSettingTab());

        root.Controls.Add(tabs, 0, 0);
        root.Controls.Add(_status, 0, 1);

        Controls.Add(root);
    }

    private TabPage CreateLaunchTab()
    {
        var tab = new TabPage("启动");
        var panel = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, Padding = new Padding(12), RowCount = 6 };
        panel.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 120));
        panel.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        panel.RowStyles.Add(new RowStyle(SizeType.Absolute, 36));
        panel.RowStyles.Add(new RowStyle(SizeType.Absolute, 36));
        panel.RowStyles.Add(new RowStyle(SizeType.Absolute, 42));
        panel.RowStyles.Add(new RowStyle(SizeType.Absolute, 42));
        panel.RowStyles.Add(new RowStyle(SizeType.Absolute, 24));
        panel.RowStyles.Add(new RowStyle(SizeType.Percent, 100));

        panel.Controls.Add(new Label { Text = "配置文件", AutoSize = true, Anchor = AnchorStyles.Left }, 0, 0);
        panel.Controls.Add(_launchProfile, 1, 0);

        panel.Controls.Add(new Label { Text = "玩家账户", AutoSize = true, Anchor = AnchorStyles.Left }, 0, 1);
        panel.Controls.Add(_launchAccount, 1, 1);

        var launchBtn = new Button { Text = "开始游戏", Dock = DockStyle.Fill };
        launchBtn.Click += (_, _) => LaunchGame();
        panel.Controls.Add(launchBtn, 1, 2);

        var dlBtn = new Button { Text = "下载最新正式版到 .minecraft", Dock = DockStyle.Fill };
        dlBtn.Click += async (_, _) => await DownloadLatestAsync();
        panel.Controls.Add(dlBtn, 1, 3);

        panel.Controls.Add(new Label { Text = "启动历史", AutoSize = true, Anchor = AnchorStyles.Left }, 0, 4);
        panel.Controls.Add(_history, 1, 5);

        _launchProfile.SelectedIndexChanged += (_, _) =>
        {
            if (_launchProfile.SelectedItem is string p)
            {
                _config.SelectedProfile = p;
                SaveConfig();
            }
        };

        _launchAccount.SelectedIndexChanged += (_, _) =>
        {
            if (_launchAccount.SelectedItem is string a)
            {
                _config.SelectedAccount = a;
                SaveConfig();
            }
        };

        tab.Controls.Add(panel);
        return tab;
    }

    private TabPage CreateProfileTab()
    {
        var tab = new TabPage("配置");
        var split = new SplitContainer { Dock = DockStyle.Fill, SplitterDistance = 280 };
        split.Panel1.Controls.Add(_profileList);

        var edit = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, Padding = new Padding(12), RowCount = 6 };
        edit.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 120));
        edit.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        for (var i = 0; i < 5; i++) edit.RowStyles.Add(new RowStyle(SizeType.Absolute, 36));
        edit.RowStyles.Add(new RowStyle(SizeType.Percent, 100));

        AddRow(edit, 0, "名称", _pName);
        AddRow(edit, 1, "版本", _pVersion);
        AddRow(edit, 2, "游戏目录", _pGameDir);
        AddRow(edit, 3, "Java 路径", _pJava);
        AddRow(edit, 4, "内存(MB)", _pMem);

        var rowButtons = new FlowLayoutPanel { Dock = DockStyle.Fill, FlowDirection = FlowDirection.LeftToRight, WrapContents = false };
        var save = new Button { Text = "保存配置", AutoSize = true };
        var add = new Button { Text = "新建配置", AutoSize = true };
        var del = new Button { Text = "删除配置", AutoSize = true };

        save.Click += (_, _) => SaveProfile();
        add.Click += (_, _) => AddProfile();
        del.Click += (_, _) => DeleteProfile();

        rowButtons.Controls.AddRange(new Control[] { save, add, del });
        edit.Controls.Add(rowButtons, 1, 5);

        split.Panel2.Controls.Add(edit);

        _profileList.SelectedIndexChanged += (_, _) => FillProfileEditor();
        tab.Controls.Add(split);
        return tab;
    }

    private TabPage CreateAccountTab()
    {
        var tab = new TabPage("账户");
        var split = new SplitContainer { Dock = DockStyle.Fill, SplitterDistance = 280 };
        split.Panel1.Controls.Add(_accountList);

        var form = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, Padding = new Padding(12), RowCount = 8 };
        form.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 120));
        form.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        for (var i = 0; i < 7; i++) form.RowStyles.Add(new RowStyle(SizeType.Absolute, 36));
        form.RowStyles.Add(new RowStyle(SizeType.Percent, 100));

        AddRow(form, 0, "用户名", _aName);
        AddRow(form, 1, "类型", _aType);

        var rowButtons = new FlowLayoutPanel { Dock = DockStyle.Fill, WrapContents = false };
        var add = new Button { Text = "添加账户", AutoSize = true };
        var del = new Button { Text = "删除账户", AutoSize = true };

        add.Click += (_, _) => AddAccount();
        del.Click += (_, _) => DeleteAccount();

        rowButtons.Controls.Add(add);
        rowButtons.Controls.Add(del);
        form.Controls.Add(rowButtons, 1, 2);

        form.Controls.Add(new Label { Text = "LittleSkin 服务器", AutoSize = true, Anchor = AnchorStyles.Left }, 0, 3);
        form.Controls.Add(_yggdrasilServer, 1, 3);
        form.Controls.Add(new Label { Text = "登录邮箱/用户名", AutoSize = true, Anchor = AnchorStyles.Left }, 0, 4);
        form.Controls.Add(_yggUsername, 1, 4);
        form.Controls.Add(new Label { Text = "密码", AutoSize = true, Anchor = AnchorStyles.Left }, 0, 5);
        form.Controls.Add(_yggPassword, 1, 5);

        var yggLoginBtn = new Button { Text = "第三方登录（LittleSkin）", Dock = DockStyle.Fill };
        yggLoginBtn.Click += async (_, _) => await LoginYggdrasilAsync();
        form.Controls.Add(yggLoginBtn, 1, 6);

        split.Panel2.Controls.Add(form);

        tab.Controls.Add(split);
        return tab;
    }

    private TabPage CreateSettingTab()
    {
        var tab = new TabPage("设置");
        var panel = new TableLayoutPanel { Dock = DockStyle.Fill, ColumnCount = 2, Padding = new Padding(12), RowCount = 3 };
        panel.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 140));
        panel.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        panel.RowStyles.Add(new RowStyle(SizeType.Absolute, 36));
        panel.RowStyles.Add(new RowStyle(SizeType.Absolute, 42));
        panel.RowStyles.Add(new RowStyle(SizeType.Percent, 100));

        AddRow(panel, 0, "保留历史条数", _keepHistory);

        var export = new Button { Text = "导出配置 JSON", Dock = DockStyle.Fill };
        export.Click += (_, _) => ExportConfig();
        panel.Controls.Add(export, 1, 1);

        _keepHistory.ValueChanged += (_, _) =>
        {
            _config.KeepHistory = (int)_keepHistory.Value;
            SaveConfig();
            BindHistory();
        };

        tab.Controls.Add(panel);
        return tab;
    }

    private static void AddRow(TableLayoutPanel panel, int row, string label, Control input)
    {
        panel.Controls.Add(new Label { Text = label, AutoSize = true, Anchor = AnchorStyles.Left }, 0, row);
        input.Dock = DockStyle.Fill;
        panel.Controls.Add(input, 1, row);
    }

    private void LoadConfig()
    {
        _config = ConfigStore.Load();
        BindAll();
    }

    private void SaveConfig()
    {
        ConfigStore.Save(_config);
    }

    private void BindAll()
    {
        _launchProfile.Items.Clear();
        _launchProfile.Items.AddRange(_config.Profiles.Select(p => p.Name).Cast<object>().ToArray());

        _launchAccount.Items.Clear();
        _launchAccount.Items.AddRange(_config.Accounts.Select(a => a.Username).Cast<object>().ToArray());

        _profileList.Items.Clear();
        _profileList.Items.AddRange(_config.Profiles.Select(p => p.Name).Cast<object>().ToArray());

        _accountList.Items.Clear();
        _accountList.Items.AddRange(_config.Accounts.Select(a => $"{a.Username} ({a.AccountType})").Cast<object>().ToArray());

        _keepHistory.Value = Math.Min(_keepHistory.Maximum, Math.Max(_keepHistory.Minimum, _config.KeepHistory));
        _yggdrasilServer.Text = _config.YggdrasilServer;

        _launchProfile.SelectedItem = _config.SelectedProfile;
        _launchAccount.SelectedItem = _config.SelectedAccount;
        if (_profileList.Items.Count > 0) _profileList.SelectedIndex = 0;

        BindHistory();
    }

    private void BindHistory()
    {
        _history.Text = string.Join(Environment.NewLine, _config.LaunchHistory.TakeLast(_config.KeepHistory));
    }

    private Profile? CurrentProfileByList()
    {
        if (_profileList.SelectedItem is not string selectedName) return null;
        return _config.Profiles.FirstOrDefault(p => p.Name == selectedName);
    }

    private void FillProfileEditor()
    {
        var p = CurrentProfileByList();
        if (p is null) return;

        _pName.Text = p.Name;
        _pVersion.Text = p.Version;
        _pGameDir.Text = p.GameDir;
        _pJava.Text = p.JavaPath;
        _pMem.Value = Math.Max(_pMem.Minimum, Math.Min(_pMem.Maximum, p.MaxMemoryMb));
    }

    private void SaveProfile()
    {
        var p = CurrentProfileByList();
        if (p is null)
        {
            MessageBox.Show("请先选中一个配置。", "提示");
            return;
        }

        var oldName = p.Name;
        p.Name = string.IsNullOrWhiteSpace(_pName.Text) ? p.Name : _pName.Text.Trim();
        p.Version = string.IsNullOrWhiteSpace(_pVersion.Text) ? p.Version : _pVersion.Text.Trim();
        p.GameDir = _pGameDir.Text.Trim();
        p.JavaPath = _pJava.Text.Trim();
        p.MaxMemoryMb = (int)_pMem.Value;

        if (_config.SelectedProfile == oldName) _config.SelectedProfile = p.Name;
        SaveConfig();
        BindAll();
    }

    private void AddProfile()
    {
        var name = $"Profile-{_config.Profiles.Count + 1}";
        _config.Profiles.Add(new Profile { Name = name, Version = "latest-release", GameDir = Path.Combine(Environment.CurrentDirectory, ".minecraft"), JavaPath = "java" });
        _config.SelectedProfile = name;
        SaveConfig();
        BindAll();
    }

    private void DeleteProfile()
    {
        var p = CurrentProfileByList();
        if (p is null) return;
        if (_config.Profiles.Count <= 1)
        {
            MessageBox.Show("至少保留一个配置。", "提示");
            return;
        }

        _config.Profiles.Remove(p);
        _config.SelectedProfile = _config.Profiles[0].Name;
        SaveConfig();
        BindAll();
    }

    private void AddAccount()
    {
        var name = _aName.Text.Trim();
        if (string.IsNullOrWhiteSpace(name))
        {
            MessageBox.Show("用户名不能为空。", "提示");
            return;
        }
        if (_config.Accounts.Any(a => a.Username.Equals(name, StringComparison.OrdinalIgnoreCase)))
        {
            MessageBox.Show("用户名已存在。", "提示");
            return;
        }

        _config.Accounts.Add(new Account { Username = name, AccountType = _aType.Text });
        _config.SelectedAccount = name;
        _aName.Clear();
        SaveConfig();
        BindAll();
    }

    private void DeleteAccount()
    {
        if (_accountList.SelectedIndex < 0) return;
        if (_config.Accounts.Count <= 1)
        {
            MessageBox.Show("至少保留一个账户。", "提示");
            return;
        }

        var account = _config.Accounts[_accountList.SelectedIndex];
        _config.Accounts.Remove(account);
        _config.SelectedAccount = _config.Accounts[0].Username;
        SaveConfig();
        BindAll();
    }

    private async Task LoginYggdrasilAsync()
    {
        var username = _yggUsername.Text.Trim();
        var password = _yggPassword.Text;
        var server = _yggdrasilServer.Text.Trim();

        if (string.IsNullOrWhiteSpace(username) || string.IsNullOrWhiteSpace(password))
        {
            MessageBox.Show("请填写 LittleSkin 账户和密码。", "提示");
            return;
        }

        SetStatus("正在登录第三方账户...");
        var (ok, message, account) = await YggdrasilAuthService.LoginAsync(server, username, password);
        if (!ok || account is null)
        {
            SetStatus("第三方登录失败");
            MessageBox.Show(message, "错误");
            return;
        }

        _config.YggdrasilServer = server;
        var existed = _config.Accounts.FirstOrDefault(a => a.Username == account.Username && a.AccountType == "yggdrasil");
        if (existed is null)
            _config.Accounts.Add(account);
        else
        {
            existed.AccessToken = account.AccessToken;
            existed.Uuid = account.Uuid;
        }

        _config.SelectedAccount = account.Username;
        SaveConfig();
        BindAll();

        SetStatus("第三方登录成功");
        MessageBox.Show(message, "提示");
    }

    private async Task DownloadLatestAsync()
    {
        var targetDir = Path.Combine(Environment.CurrentDirectory, ".minecraft");
        SetStatus("正在下载最新正式版...");

        var (ok, message, versionId) = await MinecraftDownloader.DownloadLatestReleaseAsync(targetDir);
        if (!ok)
        {
            SetStatus("下载失败");
            MessageBox.Show(message, "错误");
            return;
        }

        var defaultProfile = _config.Profiles.FirstOrDefault(p => p.Name == _config.SelectedProfile) ?? _config.Profiles[0];
        defaultProfile.GameDir = targetDir;
        if (!string.IsNullOrWhiteSpace(versionId)) defaultProfile.Version = versionId;

        SaveConfig();
        BindAll();

        SetStatus("下载完成");
        MessageBox.Show(message, "提示");
    }

    private void LaunchGame()
    {
        var profile = _config.Profiles.FirstOrDefault(p => p.Name == _config.SelectedProfile);
        if (profile is null)
        {
            MessageBox.Show("未找到配置文件。", "错误");
            return;
        }

        if (!Directory.Exists(profile.GameDir))
        {
            MessageBox.Show($"游戏目录不存在: {profile.GameDir}", "错误");
            return;
        }

        File.WriteAllText("username.txt", _config.SelectedAccount);
        File.WriteAllText("maxmb.txt", profile.MaxMemoryMb.ToString());
        File.WriteAllText("version.txt", profile.Version);

        var log = $"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] {_config.SelectedAccount} -> {profile.Name} ({profile.Version})";
        _config.LaunchHistory.Add(log);

        if (File.Exists("start_game.bat"))
        {
            try
            {
                Process.Start(new ProcessStartInfo
                {
                    FileName = "start_game.bat",
                    UseShellExecute = true,
                    WorkingDirectory = Environment.CurrentDirectory
                });
                SetStatus("已触发启动");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"启动失败: {ex.Message}", "错误");
                SetStatus("启动失败");
            }
        }
        else
        {
            MessageBox.Show("未检测到 start_game.bat，已仅保存配置。", "提示");
            SetStatus("未找到 start_game.bat");
        }

        SaveConfig();
        BindHistory();
    }

    private void ExportConfig()
    {
        using var dialog = new SaveFileDialog
        {
            Filter = "JSON|*.json",
            FileName = "pmcl-export.json"
        };

        if (dialog.ShowDialog() != DialogResult.OK) return;

        File.Copy(ConfigStore.ConfigPath, dialog.FileName, overwrite: true);
        MessageBox.Show("导出完成。", "提示");
    }

    private void SetStatus(string text)
    {
        _status.Text = $"状态: {text}";
    }
}
