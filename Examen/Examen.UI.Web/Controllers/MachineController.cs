using Microsoft.AspNetCore.Mvc;
using Examen.ApplicationCore.Domain;
using Examen.ApplicationCore.Interfaces;

namespace Examen.Web.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class MachineController : ControllerBase
    {
        private readonly IServiceMachine _serviceMachine;

        public MachineController(IServiceMachine serviceMachine)
        {
            _serviceMachine = serviceMachine;
        }

        // GET: api/Machine
        [HttpGet]
        public IActionResult GetMachines()
        {
            var machines = _serviceMachine.GetAll();
            return Ok(machines);
        }

        // GET: api/Machine/{code}
        [HttpGet("{code}")]
        public IActionResult GetMachine(string code)
        {
            var machine = _serviceMachine.GetById(code);
            if (machine == null) return NotFound();
            return Ok(machine);
        }

        // POST: api/Machine
        [HttpPost]
        public IActionResult AddMachine([FromBody] Machine machine)
        {
            if (!ModelState.IsValid) return BadRequest(ModelState);
            _serviceMachine.Add(machine);
            _serviceMachine.Commit();
            return CreatedAtAction(nameof(GetMachine), new { code = machine.CodeMachine }, machine);
        }

        // PUT: api/Machine/{code}
        [HttpPut("{code}")]
        public IActionResult UpdateMachine(string code, [FromBody] Machine machine)
        {
            if (code != machine.CodeMachine) return BadRequest();
            if (!ModelState.IsValid) return BadRequest(ModelState);

            _serviceMachine.Update(machine);
            _serviceMachine.Commit();
            return NoContent();
        }

        // DELETE: api/Machine/{code}
        [HttpDelete("{code}")]
        public IActionResult DeleteMachine(string code)
        {
            var machine = _serviceMachine.GetById(code);
            if (machine == null) return NotFound();

            _serviceMachine.Delete(machine);
            _serviceMachine.Commit();
            return NoContent();
        }
    }
}