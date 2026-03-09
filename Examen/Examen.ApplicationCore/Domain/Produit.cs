using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace Examen.ApplicationCore.Domain
{
    public class Produit
    {
        [Key]
        [StringLength(8, ErrorMessage = "Le code article doit contenir 8 caractères maximum")]
        [Required(ErrorMessage = "Le code article est obligatoire")]
        public string CodeArticle { get; set; }

        [Required(ErrorMessage = "Le nom du produit est obligatoire")]
        [StringLength(50, ErrorMessage = "Le nom ne doit pas dépasser 50 caractères")]
        public string NomProduit { get; set; }

        [Required(ErrorMessage = "La désignation est obligatoire")]
        [StringLength(100, MinimumLength = 3,
            ErrorMessage = "La désignation doit contenir entre 3 et 100 caractères")]
        public string Designation { get; set; }

        [Range(1, 100, ErrorMessage = "La taille d'échantillonnage doit être entre 1 et 100")]
        public int TailleEchantillonnage { get; set; }

        // Numéro OF : OF + 8 chiffres
        [Required]
        [RegularExpression(@"^OF\d{8}$",
            ErrorMessage = "Le NumOF doit commencer par OF suivi de 8 chiffres")]
        public string NumOF { get; set; }

        // Relation : 1 Produit → plusieurs TypeDefaut
        public ICollection<TypeDefaut> TypeDefauts { get; set; }

        // 1 Produit → N ResultatControle
        public ICollection<ResultatControle> ResultatControles { get; set; }

    }
}