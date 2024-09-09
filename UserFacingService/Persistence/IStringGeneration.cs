using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UserFacingService.Persistence
{
  internal interface IStringGeneration
  {
    string GenerateString(int charsLong);
  }
}
