package practica1;

import java.util.ArrayList;

public class Line {

    private final int T_RIGHT = 0;
    private final int T_LEFT = 1;
    private final int T_HOME = 2;
    private final int T_END = 3;

    private final ArrayList<Integer> lineData; // Input data memory
    private int targetPos; // Buffer pointing position
    private boolean inputMode; // Input mode state [ True: Insert Mode - False: OW Mode ]
    
    public Line() {
        
        this.lineData = new ArrayList<Integer>();
        this.targetPos = 0;
        this.inputMode = false;
    }


    public void updateBuffer(final int input) {

        if(this.targetPos == this.lineData.size())
            this.lineData.add(input);
        else {
            if(inputMode) // Mode insert
                this.lineData.add(this.targetPos, input);
            else    // Mode sobreescriptura
                this.lineData.set(this.targetPos, input);
        }
        this.tIncrease();
    }

    public void delete(final boolean currentTarget) {

        if(!this.lineData.isEmpty()){
            if(!currentTarget && this.targetPos > 0) // Esborra caracter esquerra posicio actual
                this.lineData.remove(this.targetPos - 1);
            else    // Esborra caracter posicio actual
                this.lineData.remove(this.targetPos);

            if(this.targetPos > 0)
                this.tDecrease();
        }
    }

    public void switchInsMode() {
        this.inputMode = !this.inputMode;
    }

    public void setTargetPos(final int target) {
        
        switch(target){
            case T_RIGHT:
                if(this.targetPos < this.lineData.size())
                    this.targetPos++;
                break;
            case T_LEFT:
                if(this.targetPos > 0)
                    this.targetPos--;
                break;
            case T_HOME:
                this.targetPos = 0;
                break;
            case T_END:
                this.targetPos = this.lineData.size();
                break;
            default:
                System.out.println("Invalid target position");
                break;
        }
    }

    public void tIncrease() {
        this.targetPos++;
    }

    public void tDecrease() {
        this.targetPos--;
    }

    public String getData() {
        
        String str = new String();
        int aux;

        for(int i = 0; i < this.lineData.size(); i++) {
            aux = this.lineData.get(i);
            str = str + Character.toString((char)aux);
        }

        return str;
    }

    public int getTargetPos() {
        return this.targetPos;
    }
}