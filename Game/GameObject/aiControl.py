from Game.GameObject.controller import Controller
import Game.play_scene as play_scene
import Game.world as world
from Game.GameObject.ball import Ball
from Game.GameObject.player import Player
from Math import Point
from Game.behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

import random


class AIControl(Controller):
    def __init__(self, client):
        super().__init__(client)
        self.build_behavior_tree()

    def update(self):
        if self.client.direction.x == 0 and self.client.direction.y == 0:
            self.client.current_state.idle()
        else:
            # self.client.current_state.run()
            if self.client.direction.x > 0:
                self.client.flip = False
            elif self.client.direction.x < 0:
                self.client.flip = True
        if self.client.current_state == self.client.tackle_state:
            return
        
        self.client.direction.x = 0
        self.client.direction.y = 0
        self.bt.run()

    def handle_event(self, event):
        pass

    def run_to_home(self):
        pass
                    
    def handle_collision(self, group, other):
        if group == "ball:player":
            self.client.catch(other)
            return
        
        if group == "player:player":
            if self.client.current_state == self.client.tackle_state and self.client.current_state.frame > 5:
                other.fall_to = self.client.tackle_to
                other.current_state.fall()
                return
            if other.current_state == other.tackle_state and other.current_state.frame > 5:
                self.client.fall_to = other.tackle_to
                self.client.current_state.fall()
                return
            if other.ball is not None:
                self.client.grab(other)
                return
            
    ################################ behavior tree ################################

    ######################### has ball #########################
    def has_ball(self):
        if self.client.ball is None:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS
        
    def run_to_goal(self):
        if self.client.team == 1 and self.client.position.x > play_scene.field.width/2-2:
            self.client.throw_half_power(0, 0)
            return BehaviorTree.SUCCESS
        elif self.client.team == 2 and self.client.position.x < -play_scene.field.width/2+2:
            self.client.throw_half_power(0, 0)
            return BehaviorTree.SUCCESS

        if self.client.stemina > 50:
            self.client.direction.x = -(self.client.team * 2 - 3)
            self.client.direction.y = 0
            self.client.current_state.run()
            return BehaviorTree.RUNNING
            # self.client.current_state.dash()
        # elif self.client.stemina > 0:
        #     self.client.current_state.run()
        else:
            self.client.throw_half_power(0, 0)
            return BehaviorTree.SUCCESS     # 사실은 FAIL이지만, FAIL이면 다음 행동으로 넘어가기 때문에 SUCCESS로 한다.
        
    def build_has_ball_behavior_tree(self):
        return Sequence("run to goal", 
                        Condition("has ball", self.has_ball), 
                        Action("run to goal", self.run_to_goal)
                        )
    
    ######################### release #########################
    def if_grab(self):
        if self.client.grabbed_opponent is not None:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        
    def release_grabbed_opponent(self):
        self.client.release()
        return BehaviorTree.SUCCESS
    
    def build_release_behavior_tree(self):
        return Sequence("release", 
                        Condition("if grab", self.if_grab), 
                        Action("release grabbed opponent", self.release_grabbed_opponent)
                        )
    
    ######################### defence #########################
    def enemy_team_has_ball(self):
        if play_scene.ball.owner is None or play_scene.ball.owner.team == self.client.team:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS
    
    def tackle_enemy(self):
        if Point.distance2(self.client.position, play_scene.ball.owner.position) < 3**2:
            self.client.tackle(play_scene.ball.owner.position.x, play_scene.ball.owner.position.y)
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        
    def chase_enemy(self):
        target = play_scene.ball.owner.position
        self.client.direction.x = target.x - self.client.position.x
        self.client.direction.y = target.y - self.client.position.y
        self.client.direction.normalize()
        self.client.current_state.run()
        return BehaviorTree.RUNNING
    
    def build_defence_behavior_tree(self):
        return Sequence("defence", 
                        Condition("enemy team has ball", self.enemy_team_has_ball), 
                        Selector("tackle or chase", 
                                 Action("tackle enemy", self.tackle_enemy),
                                 Action("chase enemy", self.chase_enemy)
                                 )
                        )
    
    ######################### release or defence #########################
    def opponent_does_not_have_ball(self):
        if self.client.grabbed_opponent is not None:
            if self.client.grabbed_opponent.ball is None:
                return BehaviorTree.SUCCESS
            else:
                return BehaviorTree.FAIL
        else:
            return BehaviorTree.FAIL
        
    def build_release_or_defence_behavior_tree(self):
        return Selector("release or defence", 
                        Sequence("release",
                                 Condition("opponent does not have ball", self.opponent_does_not_have_ball), 
                                 Action("release grabbed opponent", self.release_grabbed_opponent)
                                 ),
                        self.build_defence_behavior_tree()
                        )
        
    ######################### ball is free #########################
    def ball_is_free(self):
        if play_scene.ball.owner is None:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        
    def run_to_ball(self):
        target = play_scene.ball.position
        self.client.direction.x = target.x - self.client.position.x
        self.client.direction.y = target.y - self.client.position.y
        self.client.direction.normalize()
        self.client.current_state.run()
        return BehaviorTree.RUNNING

    def build_ball_is_free_behavior_tree(self):
        return Sequence("release and run to ball", 
                        Condition("ball is free", self.ball_is_free), 
                        Action("run to ball", self.run_to_ball)
                        )
    
    ######################### idle #########################
    def idle(self):
        self.client.current_state.idle()
        return BehaviorTree.SUCCESS

    ######################### build behavior tree #########################
    def build_behavior_tree(self):
        self.bt = BehaviorTree(
            Selector("AI Control",
                self.build_has_ball_behavior_tree(),
                self.build_release_or_defence_behavior_tree(),
                self.build_ball_is_free_behavior_tree(),
                Action("idle", self.idle)
            )
        )
