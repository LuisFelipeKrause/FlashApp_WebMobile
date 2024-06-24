import { Data } from "@angular/router";

export class Deck {
    public id: number;
    public usuario: number;
    public titulo: string;
    public descricao: string|undefined;
    public erros: number;
    public acertos: number;
    public num_cards: number;
    public desempenho_geral: number;

    constructor(){
        this.id = 0;
        this.usuario = 0;
        this.titulo = "";
        this.descricao = "";
        this.erros = 0;
        this.acertos = 0;
        this.num_cards = 0;
        this.desempenho_geral = 0;
    }
}