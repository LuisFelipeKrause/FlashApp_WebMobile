export class Card {
    public id: number;
    public deck: number;
    public frente: string;
    public verso: string|undefined;


    constructor(){
        this.id = 0;
        this.deck = 0;
        this.frente = "";
        this.verso = "";
    }
}