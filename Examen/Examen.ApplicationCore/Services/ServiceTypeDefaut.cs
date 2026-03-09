using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Examen.ApplicationCore.Domain;
using Examen.ApplicationCore.Interfaces;

namespace Examen.ApplicationCore.Services
{
    public class ServiceTypeDefaut : Service<TypeDefaut>, IServiceTypeDefaut
    {
        public ServiceTypeDefaut(IUnitOfWork unitOfWork) : base(unitOfWork)
        {
        }
    }
}
