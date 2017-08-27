/*
 *
 * Retra Control and Integration
 *  
 * Uses wiringPi library
 *
 * Stages:
 * (1) read stimulus and pulse protocols (stimulus = %intensity values)
 * (2) TODO: Convert stimulus protocol (int) to pairs of unsigned chars
 * (3) Loop over stimuli: if non-zero stimulus --> execute pulse
 *      (4) Inner Loop / Pulse: loop thru the pulse protocol
 *
 *
 * TODO: get rid of length params and shit --> use sizeof
 * ...and read till eof
 *
 *
 *
 */

#include <wiringPi.h>
#include <wiringSerial.h>
#include <stdio.h>
#include <stdlib.h>



// TODO: Initialize Communication to Retra and SPIM
// 3 Comms: (1) Serial to Retra, (2) TTL output to Retra, (3) TTL input from SPIM
// returns file descriptor for serial port
// red_intense should be in hex format (hmmm...could maybe be in decimal as well) 

int init_comm(){
    // broadcom numbering:
    wiringPiSetupGpio();
    // Input pin from SPIM:
    pinMode(4, INPUT);
    // Output pin to Retra (for TTL):
    pinMode(TEMP, OUTPUT); // TODO: which pin for output?
    // Initialize Serial Communication with Retra: TODO:
    int fd; 
    fd = serialOpen("/dev/ttyUSB0", 9600); // TODO: correct BAUD?   
    printf(succ); 
    // TODO: initialize and turn Retra on / set intensity to 0:
    unsigned char init1[] = {87, 2, 170, 80}; 
    unsigned char init2[] = {87, 3, 170, 80}; 
    unsigned char red_on[] = {79, 254, 80};  
    unsigned char red0[] = {83, 24, 3, 7, 255, 240, 80}; 
    serialPuts(fd, init1);
    serialPuts(fd, init2);
    serialPuts(fd, red_on); 
    serialPuts(fd, red0);
    // Set Retra to inactive high:
    digitalWrite(TEMP, HIGH);
    return fd
}



// Read from SPIM:
// returns 1 if high, 0 else
int read_SPIM(){
    return digitalRead(4); 
}



// TODO: write TTL to Retra:
void retra_ON(){
    digitalWrite(TEMP, LOW);
}

void retra_OFF(){
    digitalWrite(TEMP, HIGH); 
}



// TODO: convert int intensity values to pairs of unsigned chars:
// assumes uc declared properly and signals are in representable range (0-100)
void convert_signal_uc(int * sig, int sig_len, unsigned char * sig_uc){
    int i;
    float full_intense; float inv_intense; 
    unsigned char large_byte; unsigned char little_byte;
    for(i=0; i<sig_len; i++){
        // full intensity:
        full_intense = (float)sig[i] * (255.0/100.0); 
        // invert it:
        inv_intense = 255.0 - full_intense;
        // convert to 2 unsigned chars:
        large_byte = ((int)inv_intense) / 16; 
        little_byte = ((int)inv_intense) - (16 * large_byte);
        large_byte = 240 + large_byte; 
        sig_uc[2*i] = large_byte;
        sig_uc[2*i + 1] = little_byte * 16;  
    }
}


// TODO: write intensity to serial:
// ind = outer loop number (where we are in integer signal) 
void write_retra_serial(int fd, unsigned char * sig_uc, int ind){
    unsigned char red_intense[] = {83, 24, 3, 7, 255, 240, 80}; 
    unsigned char red_pre[] = {83, 24, 3, 7};
    unsigned char red_sig[2];
    red_sig[0] = sig_uc[ind*2];
    red_sig[1] = sig_uc[ind*2 + 1]; 
    unsigned char red_post[] = {50}; 
    serialPuts(fd, red_pre);
    serialPuts(fd, red_sig);
    serialPuts(fd, red_post); 
}



// TODO: execute pulse...take in pulse profile of 1s and 0s 
// pulse_len = length of pulse_profile
// time_scale = switching time in milliseconds 
void exec_pulse(int * pulse_profile, int time_scale, int pulse_len){
    ind = 0;
    unsigned int t0;
    unsigned int t1;
    int pulse_val; 
    t0 = millis(); 
    while(ind < pulse_len){
        // calculate ind: TODO:will this work?
        t1 = millis(); 
        ind = (t1 - t0) / time_scale;
        if(ind < pulse_len){
            // get pulse val from pulse_profile:
            pulse_val = pulse_profile[ind];
            if(pulse_val == 1){
                retra_ON();
            }
            if(pulse_val == 0){
                retra_OFF();
            }
        }
    }
    retra_OFF();
}




// TODO: run the experiment
// TODO: figure out time_scale_sub from time_scale_super and len of pulse profile
// execute pulses when seq > 0 
// update intensity when it changes:
void exec_experiment(int fd, unsigned char * seq, int time_scale_super, int * pulse_profile, int seq_len, int pulse_len){
    ind = 0;
    unsigned int t0;
    unsigned int t1; 
    int time_scale_sub = seq_len / pulse_len; 
    unsigned char byte1; unsigned char byte2; 
    unsigned char old_byte1 = 255; unsigned char old_byte2 = 240; 
    int seq_val;
    int prev_ind = 0; 
    t0 = millis();
    while(ind < seq_len){
        t1 = millis();
        ind = (t1 - t0) / time_scale_super;
        
        // only do stuff if we've moved into new time bin
        if(ind == prev_ind){
            continue; 
        }
        else{
            prev_ind = ind; 
        }

        if(ind < seq_len){
            // get the next bytes:
            byte1 = seq[2*ind];
            byte2 = seq[2*ind + 1];
        
            // if bytes are different --> change stim intensity: // TODO: won't this system lead to big delays?
            if(byte1 != old_byte1 || byte2 != old_byte2){
                write_retra_serial(fd, seq, ind);      
                old_byte1 = byte1; old_byte2 = byte2; 
            }
            
            // if stim strength > 0 --> execute pulse:
            // TODO: not sure if this is a legal comparison
            if(byte1 > 0 || byte2 > 0){ 
                exec_pulse(pulse_profile, time_scale_sub, pulse_len); 
            }
        }
    }
}




// TODO: configure run parameters
// TODO: easiest way to read in data?
// read comma separated file into array of integers:
int read_csf(const char * fn, int ** seq){
    FILE * input = fopen(fn, "r"); 

    // iterate thru once to get count: TODO: do we need an array to write into?
    int count = 0;
    int holder_val;
    while(fscanf(input,"%d%*c",&holder_val) == 1){
        count ++;
    }

    // reopen file:
    input = fopen(fn, "r"); 

    // iterate thru to get data:
    *seq = (int *)malloc(count * sizeof(int)); 
    int i = 0;
    for(i=0; i<count; i++){
        fscanf(input, "%d%*c", &((*seq)[i])); 
    }

    return count; 
}





// Master: TODO: setup and run everything
// TODO: check that pulse timing and works out??? calculate pulse_len by comparing timescales
void master(int seq_tscale){
    // set up raspi:
    int fd; 
    //Tfd = init_comm(); 
    
    // load in pulse profile:
    int * pulse_profile;
    int pulse_len;
    pulse_len = read_csf("pulse_profile.txt", &pulse_profile);
    
    // load in sequence:
    int * seq;
    int seq_len;
    seq_len = read_csf("sequence.txt", &seq); 

    printf("pulse_len = %d\n", pulse_len);
    printf("seq_len = %d\n", seq_len); 

    
    // Testing: read the sequences:
    int i;
    for(i=0; i<pulse_len; i++){
        printf("%d\n", pulse_profile[i]); 
    }
    for(i=0; i<seq_len; i++){
        printf("%d\n", seq[i]); 
    } 
    

    
    // convert sequence to unsigned char:
    unsigned char seq_uc[2 * seq_len]; 
    convert_signal_uc(seq, seq_len, seq_uc);

    // TESTING: print the conversion:
    for(i=0; i<seq_len; i++){
        printf("%u,%u\n", seq_uc[2*i], seq_uc[2*i + 1]); 
    }
    

    // TODO: wait for SPIM communication...synchronizes
    int c;
    while(!read_SPIM()){
        c = 1; 
    }

    // begin execution:
    exec_experiment(fd, seq_uc, seq_tscale, pulse_profile, seq_len, pulse_len); 

}



int main(){
    
    int seq_tscale = 500; // switch sequences every 500 ms
    master(seq_tscale);

}












