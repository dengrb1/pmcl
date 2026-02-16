using System.Net.Http.Json;
using System.Text.Json;

namespace PMCL.App;

public static class MinecraftDownloader
{
    private static readonly HttpClient Client = new();

    public static async Task<(bool ok, string message, string? versionId)> DownloadLatestReleaseAsync(string gameDir)
    {
        try
        {
            Directory.CreateDirectory(gameDir);
            var manifestUrl = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json";
            var manifest = await Client.GetFromJsonAsync<VersionManifest>(manifestUrl);
            if (manifest is null)
                return (false, "无法读取版本清单。", null);

            var latestId = manifest.Latest.Release;
            var versionMeta = manifest.Versions.FirstOrDefault(v => v.Id == latestId);
            if (versionMeta is null)
                return (false, "未找到最新正式版元数据。", null);

            var versionJsonText = await Client.GetStringAsync(versionMeta.Url);
            using var doc = JsonDocument.Parse(versionJsonText);
            if (!doc.RootElement.TryGetProperty("downloads", out var downloads) ||
                !downloads.TryGetProperty("client", out var clientInfo) ||
                !clientInfo.TryGetProperty("url", out var clientUrlNode))
            {
                return (false, "版本元数据缺少客户端下载地址。", null);
            }

            var clientUrl = clientUrlNode.GetString();
            if (string.IsNullOrWhiteSpace(clientUrl))
                return (false, "客户端下载地址为空。", null);

            var versionDir = Path.Combine(gameDir, "versions", latestId);
            Directory.CreateDirectory(versionDir);

            var jsonPath = Path.Combine(versionDir, $"{latestId}.json");
            var jarPath = Path.Combine(versionDir, $"{latestId}.jar");

            await File.WriteAllTextAsync(jsonPath, versionJsonText);

            await using (var stream = await Client.GetStreamAsync(clientUrl))
            await using (var output = File.Create(jarPath))
            {
                await stream.CopyToAsync(output);
            }

            return (true, $"已下载最新正式版 {latestId} 到 {versionDir}", latestId);
        }
        catch (Exception ex)
        {
            return (false, $"下载失败: {ex.Message}", null);
        }
    }

    private sealed class VersionManifest
    {
        public required LatestInfo Latest { get; set; }
        public required List<VersionInfo> Versions { get; set; }
    }

    private sealed class LatestInfo
    {
        public required string Release { get; set; }
        public required string Snapshot { get; set; }
    }

    private sealed class VersionInfo
    {
        public required string Id { get; set; }
        public required string Type { get; set; }
        public required string Url { get; set; }
    }
}

public static class YggdrasilAuthService
{
    private static readonly HttpClient Client = new();

    public static async Task<(bool ok, string message, Account? account)> LoginAsync(
        string serverBase,
        string username,
        string password)
    {
        try
        {
            if (string.IsNullOrWhiteSpace(serverBase))
                return (false, "Yggdrasil 服务地址不能为空。", null);

            var endpoint = serverBase.TrimEnd('/') + "/authserver/authenticate";
            var payload = new
            {
                agent = new { name = "Minecraft", version = 1 },
                username,
                password,
                requestUser = true
            };

            using var response = await Client.PostAsJsonAsync(endpoint, payload);
            var body = await response.Content.ReadAsStringAsync();

            if (!response.IsSuccessStatusCode)
                return (false, $"登录失败: {response.StatusCode} {body}", null);

            using var doc = JsonDocument.Parse(body);
            var root = doc.RootElement;

            var token = root.GetProperty("accessToken").GetString() ?? string.Empty;
            var profile = root.GetProperty("selectedProfile");
            var uuid = profile.GetProperty("id").GetString() ?? string.Empty;
            var name = profile.GetProperty("name").GetString() ?? username;

            return (true, "第三方账户登录成功。", new Account
            {
                Username = name,
                AccountType = "yggdrasil",
                AccessToken = token,
                Uuid = uuid
            });
        }
        catch (Exception ex)
        {
            return (false, $"登录失败: {ex.Message}", null);
        }
    }
}
