using System.Collections.Generic;
using Examen.ApplicationCore.Domain;
using Examen.ApplicationCore.Interfaces;

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
            Commit();
        }

        public void Update(Machine machine)
        {
            _unitOfWork.Repository<Machine>().Update(machine);
            Commit();
        }

        public void Delete(Machine machine)
        {
            _unitOfWork.Repository<Machine>().Delete(machine);
            Commit();
        }

        public void Commit()
        {
            _unitOfWork.Save(); // valide les changements
        }
    }
}