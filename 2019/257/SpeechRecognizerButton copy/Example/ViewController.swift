//
//  ViewController.swift
//  Example
//
//  Created by Alejandro Ruperez Hernando on 26/2/18.
//  Copyright © 2018 alexruperez. All rights reserved.
//

import UIKit
import SpeechRecognizerButton

class ViewController: UIViewController {
  
  @IBOutlet weak var label: UILabel!
  @IBOutlet weak var button: SFButton!
  
  override func viewDidLoad() {
    super.viewDidLoad()
    
    //button.authorizationErrorHandling = .openSettings(completion: nil)
    button.resultHandler = {
      let array = $1?.bestTranscription.formattedString.components(separatedBy: " ")
      let result = array?.joined(separator: "👏")
      self.label.text = result
      //self.button.play()
      
      for word in array ?? [""] {
        let utterance = AVSpeechUtterance(string: word)
        utterance.voice = AVSpeechSynthesisVoice(language: "en-GB")
        utterance.rate = 0.6
        
        let synthesizer = AVSpeechSynthesizer()
        synthesizer.speak(utterance)
        self.playSound()
        usleep(800000)
      }
    }
    button.errorHandler = {
      self.label.text = $0?.localizedDescription
    }
  }
  
  var player: AVAudioPlayer?
  
  func playSound() {
    guard let url = Bundle.main.url(forResource: "clap", withExtension: "wav") else { return }
    
    do {
      try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default)
      try AVAudioSession.sharedInstance().setActive(true)
      
      /* The following line is required for the player to work on iOS 11. Change the file type accordingly*/
      player = try AVAudioPlayer(contentsOf: url, fileTypeHint: AVFileType.mp3.rawValue)
      
      /* iOS 10 and earlier require the following line:
       player = try AVAudioPlayer(contentsOf: url, fileTypeHint: AVFileTypeMPEGLayer3) */
      
      guard let player = player else { return }
      
      player.play()
      
    } catch let error {
      print(error.localizedDescription)
    }
  }
  
}
