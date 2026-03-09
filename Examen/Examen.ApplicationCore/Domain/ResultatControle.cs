using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Examen.ApplicationCore.Domain
{
    public class ResultatControle
    {
        [Key]
        [Required]
        [RegularExpression(@"^RC\d{5}$",
            ErrorMessage = "L'id doit commencer par RC suivi de 5 chiffres")]
        public string Id { get; set; }

        [Range(1, 100, ErrorMessage = "Nombre d'échantillons invalide")]
        public int NbEchantillons { get; set; }

        [Required]
        [DataType(DataType.Date)]
        [Display(Name = "Date de Controle")]
        public DateTime DateControle { get; set; }

        [Required]
        [RegularExpression(@"^(Conforme|Non Conforme)$",
            ErrorMessage = "Statut doit être Conforme ou Non Conforme")]
        public string StatutLot { get; set; }

        //  Relation avec Machine
        [ForeignKey("Machine")]
        public string CodeMachine { get; set; }
        public Machine Machine { get; set; }

        //  Relation avec Produit
        [ForeignKey("Produit")]
        public string CodeArticle { get; set; }
        public Produit Produit { get; set; }

        //  Relation avec Utilisateur
        [ForeignKey("Utilisateur")]
        public int UtilisateurId { get; set; }
        public Utilisateur Utilisateur { get; set; }
    }
}