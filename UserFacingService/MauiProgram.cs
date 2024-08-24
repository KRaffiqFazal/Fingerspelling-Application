using Manuela;
using Microsoft.Extensions.Logging;

namespace UserFacingService
{
  public static class MauiProgram
  {
    public static MauiApp CreateMauiApp()
    {
      var builder = MauiApp.CreateBuilder();
      builder
          .UseMauiApp<App>()
          .ConfigureFonts(fonts =>
          {
            fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
          })
          .UseManuela();

      builder.Services.AddMauiBlazorWebView();


      return builder.Build();
    }
  }
}
