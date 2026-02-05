using System.Text.Json;
using System.Text.Json.Serialization;

namespace PMCL.App;

public sealed class Account
{
    public string Username { get; set; } = "Steve";
    public string AccountType { get; set; } = "offline";
}

public sealed class Profile
{
    public string Name { get; set; } = "Default";
    public string Version { get; set; } = "1.8.9 Forge";
    public string GameDir { get; set; } = Path.Combine(Environment.CurrentDirectory, ".minecraft");
    public string JavaPath { get; set; } = Path.Combine(Environment.CurrentDirectory, "jre-x64", "bin", "java.exe");
    public int MaxMemoryMb { get; set; } = 2048;
    public int Width { get; set; } = 854;
    public int Height { get; set; } = 480;
    public string JvmArgs { get; set; } = string.Empty;
}

public sealed class LauncherConfig
{
    public string SelectedProfile { get; set; } = "Default";
    public string SelectedAccount { get; set; } = "Steve";
    public int KeepHistory { get; set; } = 100;
    public List<Account> Accounts { get; set; } = new() { new Account() };
    public List<Profile> Profiles { get; set; } = new() { new Profile() };
    public List<string> LaunchHistory { get; set; } = new();
}

public static class ConfigStore
{
    public static readonly string ConfigPath = Path.Combine(Environment.CurrentDirectory, "launcher-config.json");

    public static LauncherConfig Load()
    {
        if (!File.Exists(ConfigPath))
        {
            var initial = new LauncherConfig();
            Save(initial);
            return initial;
        }

        var json = File.ReadAllText(ConfigPath);
        var cfg = JsonSerializer.Deserialize<LauncherConfig>(json, JsonOptions()) ?? new LauncherConfig();

        if (cfg.Accounts.Count == 0) cfg.Accounts.Add(new Account());
        if (cfg.Profiles.Count == 0) cfg.Profiles.Add(new Profile());
        if (string.IsNullOrWhiteSpace(cfg.SelectedAccount)) cfg.SelectedAccount = cfg.Accounts[0].Username;
        if (string.IsNullOrWhiteSpace(cfg.SelectedProfile)) cfg.SelectedProfile = cfg.Profiles[0].Name;

        return cfg;
    }

    public static void Save(LauncherConfig cfg)
    {
        var keep = Math.Max(10, cfg.KeepHistory);
        cfg.LaunchHistory = cfg.LaunchHistory.TakeLast(keep).ToList();

        var json = JsonSerializer.Serialize(cfg, JsonOptions());
        File.WriteAllText(ConfigPath, json);
    }

    static JsonSerializerOptions JsonOptions() => new()
    {
        WriteIndented = true,
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull
    };
}
