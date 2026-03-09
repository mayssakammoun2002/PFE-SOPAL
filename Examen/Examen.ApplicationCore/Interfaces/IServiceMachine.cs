using Examen.ApplicationCore.Domain;
using Examen.ApplicationCore.Interfaces;
using Examen.ApplicationCore.Services;
using System.Collections.Generic;

public interface IServiceMachine
{
    IEnumerable<Machine> GetAll();
    Machine GetById(string codeMachine);
    void Add(Machine machine);
    void Update(Machine machine);
    void Delete(Machine machine);
    void Commit();
}