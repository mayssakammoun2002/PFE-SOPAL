using Examen.ApplicationCore.Domain;
using System.Collections.Generic;

namespace Examen.ApplicationCore.Interfaces
{
    internal interface IMachineRepository
    {
        IEnumerable<Machine> GetAll();            // Récupérer toutes les machines
        Machine GetById(string codeMachine);      // Récupérer une machine par code
        void Add(Machine machine);                // Ajouter une machine
        void Update(Machine machine);             // Mettre à jour une machine
        void Delete(Machine machine);             // Supprimer une machine
    }
}