using Examen.ApplicationCore.Domain;
using Examen.ApplicationCore.Interfaces;
using System.Collections.Generic;

namespace Examen.ApplicationCore.Services
{
    public class ServiceMachine : IServiceMachine
    {
        private readonly IUnitOfWork _unitOfWork;

        public ServiceMachine(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        public IEnumerable<Machine> GetAll()
        {
            return _unitOfWork.Repository<Machine>().GetAll();
        }

        public Machine GetById(string codeMachine)
        {
            return _unitOfWork.Repository<Machine>().GetById(codeMachine);
        }

        public void Add(Machine machine)
        {
            _unitOfWork.Repository<Machine>().Add(machine);
            Commit(); // on sauvegarde
        }

        public void Update(Machine machine)
        {
            _unitOfWork.Repository<Machine>().Update(machine);
            Commit(); // on sauvegarde
        }

        public void Delete(Machine machine)
        {
            _unitOfWork.Repository<Machine>().Delete(machine);
            Commit(); // on sauvegarde
        }

        // ✅ Implémentation de Commit() pour respecter l'interface
        public void Commit()
        {
            _unitOfWork.Save();
        }
    }
}