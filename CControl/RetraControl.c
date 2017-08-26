/*
 *
 * Retra Control and Integration
 *  
 * Uses wiringPi library
 *
 * (1) Constant light intensity value
 * (2) Triggers ttl pulses to turn light on and off (millisecond resolution)
 *
 *
 * Input: array of integers (space bad, but easy to look up...low error...)  AND timescale 
 * NOTE: raspi timing now completely separate from SPIM (except for init) 
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
int init_comm(unsigned char red_intense1, unsigned_char red_intense2){
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
    // TODO: initialize and turn Retra on...use hex
    unsigned char init1[] = {0x57, 0x02, 0xFF, 0x50}; 
    unsigned char init2[] = {0x57, 0x03, 0xAB, 0x50}; 
    unsigned char red_on[] = {0x4F, 0xFE, 0x50}; 
    unsigned char red_level[] = {0x53, 0x18, 0x3, 0x7, red_intense1, red_intense2, 0x50};
    serialPuts(fd, init1);
    serialPuts(fd, init2);
    serialPuts(fd, red_on); 
    serialPuts(fd, red_level);
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




// TODO: execute pulse...take in pulse profile of 1s and 0s 
// pulse_len = length of pulse_profile
// time_scale = switching time in milliseconds 
void exec_pulse(int * pulse_profile, int pulse_len, int time_scale){
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
// execute pulses when seq = 1:
void exec_experiment(int * seq, int seq_len, int time_scale_super, int * pulse_profile, int pulse_len, int time_scale_sub){
    ind = 0;
    unsigned int t0;
    unsigned int t1; 
    int seq_val;
    t0 = millis();
    while(ind < seq_len){
        t1 = millis();
        ind = (t1 - t0) / time_scale_super;
        if(ind < seq_len){
            seq_val = seq[ind];
            if(seq_val == 1){
                exec_pulse(pulse_profile, pulse_len, time_scale_sub);
            }
        }
    }
}




// TODO: configure run parameters
// TODO: easiest way to read in data?
// read comma separated file into array of integers:
void read_csf(fn, int * seq, int seq_len){
    int i = 0;
    for(i=0; i<seq_len; i++){
        fscanf(fn, "%d", seq[i]); 
    }
}





// Master: TODO: setup and run everything
// TODO: check that pulse timing and works out??? calculate pulse_len by comparing timescales
void master(unsigned char red_intense1, unsigned char red_intense2, int seq_len, int seq_tscale, int pulse_tscale){
    // set up raspi:
    fp = init_comm(red_intense1, red_intense2);
    // calculate pulse_len by comparing timescales:
    int pulse_len = (seq_tscale / pulse_tscale); // TODO: is this consistent with pulse execution?
    
    // load in pulse profile:
    int * pulse_profile;
    read_csf("pulse_profile.txt", pulse_profile, pulse_len);
    // load in sequence:
    int * seq;
    read_csf("sequence.txt", seq, seq_len);

    // begin execution:
    exec_experiment(seq, seq_len, seq_tscale, pulse_profile, pulse_len, pulse_tscale); 

}












