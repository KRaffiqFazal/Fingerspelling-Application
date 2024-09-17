using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Xamarin.Google.Crypto.Tink.Internal;
using Random = System.Random;

namespace UserFacingService.Persistence;

internal class RandomChars : IStringGeneration
{
    private const string c_alphabet = "abcdefghijklmnopqrstuvwxyz";

    public string GenerateString(int charsLong)
    {
        var stringOfChars = new StringBuilder(charsLong);

        var randomGen = new Random();

        for (var i = 1; i <= charsLong; i++)
        {
            stringOfChars.Append(c_alphabet[randomGen.Next(0, c_alphabet.Length - 1)]);
        }

        return stringOfChars.ToString();
    }
}