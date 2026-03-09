using System.ComponentModel.DataAnnotations;

namespace Examen.ApplicationCore.Domain
{
    public class Machine
    {
        [Key]
        [Required]
        [StringLength(8, ErrorMessage = "Le code machine doit contenir 8 caractères")]
        public string CodeMachine { get; set; }

        [Required(ErrorMessage = "Le nom machine est obligatoire")]
        [StringLength(50)]
        public string NomMachine { get; set; }

        public bool Actif { get; set; }
        //Bidirectionnel
    public ICollection<ResultatControle> ResultatControles { get; set; }
    }
}