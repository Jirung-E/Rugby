from Game.GameObject.controller import Controller
import Game.play_scene as play_scene
import Game.game_framework as game_framework
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
        self.__bt_update_delay = 0.4
        self.__times = random.uniform(0, self.__bt_update_delay)

    def update(self):
        if self.client.direction.x > 0:
            self.client.flip = False
        elif self.client.direction.x < 0:
            self.client.flip = True

        if self.client.current_state == self.client.fall_state or self.client.current_state == self.client.tackle_state:
            self.client.release()
            return

        self.__times += game_framework.dt
        if self.__times >= self.__bt_update_delay:
            self.__times = 0
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
            if other.ball is None:
                return 
            if self.client.current_state == self.client.tackle_state or self.client.current_state == self.client.fall_state:
                return
            self.client.grab(other)
            return
            
    ################################ behavior tree ################################

    ######################### has ball #########################
    def has_ball(self):
        if self.client.ball is None:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS
    
    def not_grabbed(self):
        if self.client.attackers:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS

    def run_to_goal(self):
        if self.client.team == 1 and self.client.position.x > play_scene.field.width/2-2:
            return BehaviorTree.SUCCESS
        elif self.client.team == 2 and self.client.position.x < -play_scene.field.width/2+2:
            return BehaviorTree.SUCCESS

        self.client.direction.x = -(self.client.team * 2 - 3)
        self.client.direction.y = 0
        if self.client.stemina < 50:
            self.client.current_state.run()
        else:
            self.client.current_state.dash()
        return BehaviorTree.RUNNING
    
    def tackle_forwards(self):
        if self.client.stemina < 50:
            return BehaviorTree.FAIL
        self.client.tackle(play_scene.ball.owner.position.x + (3 - self.client.team * 2), self.client.position.y)
        return BehaviorTree.SUCCESS
    
    def pass_to_team(self):
        nearest = None
        nearest_distance = 1000000
        for p in play_scene.team[self.client.team-1]:
            if p is self.client:
                continue
            if self.client.team == 1 and p.position.x > self.client.position.x:
                if nearest is None:
                    nearest = p
                else:
                    dist = Point.distance2(self.client.position, p.position)
                    if dist < nearest_distance:
                        nearest = p
                        nearest_distance = dist
            elif self.client.team == 2 and p.position.x < self.client.position.x:
                if nearest is None:
                    nearest = p
                else:
                    dist = Point.distance2(self.client.position, p.position)
                    if dist < nearest_distance:
                        nearest = p
                        nearest_distance = dist
        if nearest is not None:
            self.client.throw(nearest.position.x, nearest.position.y)
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL
    
    def hold(self):
        return BehaviorTree.SUCCESS
        
    def build_try_to_goal_behavior_tree(self):
        return Sequence("try to goal", 
                        Condition("has ball", self.has_ball), 
                        Selector("run or tackle or pass or hold", 
                                 Sequence("try to run", 
                                          Condition("not grabbed", self.not_grabbed),
                                          Action("run to goal", self.run_to_goal)
                                          ),
                                 Sequence("try to tackle",
                                          Action("tackle", self.tackle_forwards)
                                          ),
                                 Sequence("try to pass", 
                                          Action("pass", self.pass_to_team)
                                          ),
                                 Action("hold", self.hold)
                                 )
                        )
    
    ######################### team has ball #########################
    def team_has_ball(self):        # 팀원이 공을 잡고있다면
        if play_scene.ball.owner is None:
            return BehaviorTree.FAIL
        
        if play_scene.ball.owner.team == self.client.team:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        
    def is_owner_was_grabbed(self): # 공을 잡은 플레이어가 상대팀에게 잡혔다면
        if play_scene.ball.owner.attackers:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        
    def save_owner(self):           # 공을 잡은 플레이어를 구하러 간다
        if self.client.stemina < 50 or abs(self.client.y_fix - play_scene.ball.owner.position.y) > 2:
            return BehaviorTree.FAIL
        
        target = play_scene.ball.owner.position
        if Point.distance2(self.client.position, target) < 2**2:
            self.client.tackle(target.x, target.y)
            return BehaviorTree.SUCCESS
        
        # self.client.direction.x = target.x - self.client.position.x
        # self.client.direction.y = target.y - self.client.position.y
        # self.client.direction.normalize()
        if self.client.stemina < 60:
            self.client.current_state.run()
        else:
            self.client.current_state.dash()
        return BehaviorTree.RUNNING
    
    def run_parallel(self):
        x_distance = abs(self.client.position.x - play_scene.ball.owner.position.x)
        if self.client.team == 1:
            if self.client.position.x < play_scene.ball.owner.position.x and x_distance < 1:
                return BehaviorTree.SUCCESS 
            else:
                self.client.direction.x = play_scene.ball.owner.position.x-1 - self.client.position.x
        elif self.client.team == 2:
            if self.client.position.x > play_scene.ball.owner.position.x and x_distance < 1:
                return BehaviorTree.SUCCESS
            else:
                self.client.direction.x = play_scene.ball.owner.position.x+1 - self.client.position.x
            
        self.client.direction.y = self.client.y_fix - self.client.position.y
        self.client.direction.normalize()
        self.client.current_state.run()
        return BehaviorTree.RUNNING
    
    def build_support_team_behavior_tree(self):
        return Sequence("support team", 
                        Condition("team has ball", self.team_has_ball), 
                        Selector("try to support", 
                                 Sequence("try to save", 
                                          Condition("is owner was grabbed", self.is_owner_was_grabbed), 
                                          Action("save owner", self.save_owner)
                                          ),
                                 Action("run parallel", self.run_parallel)
                                 )
                        )

    ######################### release #########################
    def if_grab(self):
        if self.client.grabbed_opponent is not None:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        
    def opponent_does_not_have_ball(self):
        if self.client.grabbed_opponent.ball is None:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        
    def release_grabbed_opponent(self):
        self.client.release()
        return BehaviorTree.SUCCESS
    
    def build_release_behavior_tree(self):
        return Sequence("release",
                        Condition("if grab", self.if_grab),
                        Condition("opponent does not have ball", self.opponent_does_not_have_ball), 
                        Action("release grabbed opponent", self.release_grabbed_opponent)
                        )
    
    ######################### defence #########################
    def enemy_team_has_ball(self):
        if play_scene.ball.owner is None:
            return BehaviorTree.FAIL
        
        if play_scene.ball.owner.team == self.client.team:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS
    
    def tackle_enemy(self):
        if self.client.stemina < 50:
            return BehaviorTree.FAIL
        if Point.distance2(self.client.position, play_scene.ball.owner.position) < 2**2:
            self.client.tackle(play_scene.ball.owner.position.x, play_scene.ball.owner.position.y)
            return BehaviorTree.RUNNING     # 이부분이 SUCCESS면 이 이후 동작이 멈춘다. 이유는 모름
        else:
            return BehaviorTree.FAIL
        
    def chase_enemy(self):
        target = play_scene.ball.owner.position
        self.client.direction.x = target.x - self.client.position.x
        if Point.distance2(self.client.position, play_scene.ball.owner.position) < 1.5**2:
            self.client.direction.y = target.y - self.client.position.y
        else:
            self.client.direction.y = self.client.y_fix - self.client.position.y
        self.client.direction.normalize()
        if self.client.stemina < 50:
            self.client.current_state.run()
        else:
            self.client.current_state.dash()
        return BehaviorTree.RUNNING
    
    def build_defence_behavior_tree(self):
        return Sequence("defence", 
                        Condition("enemy team has ball", self.enemy_team_has_ball), 
                        Selector("tackle or chase", 
                                 Action("tackle enemy", self.tackle_enemy),
                                 Action("chase enemy", self.chase_enemy)
                                 )
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
        if abs(self.client.y_fix - target.y) > 2:
            self.client.direction.y = 0
        else:
            self.client.direction.y = target.y - self.client.position.y
        self.client.direction.normalize()

        if self.client.stemina < 50:
            self.client.current_state.run()
        else:
            self.client.current_state.dash()

        return BehaviorTree.RUNNING

    def build_ball_is_free_behavior_tree(self):
        return Sequence("release and run to ball", 
                        Condition("ball is free", self.ball_is_free), 
                        Action("run to ball", self.run_to_ball)
                        )

    ######################### idle #########################
    def idle(self):
        self.client.direction.x = 0
        self.client.direction.y = 0
        self.client.current_state.idle()
        return BehaviorTree.SUCCESS

    ######################### build behavior tree #########################
    def build_behavior_tree(self):
        self.bt = BehaviorTree(
            Selector("AI Control",
                self.build_try_to_goal_behavior_tree(),
                self.build_support_team_behavior_tree(),
                self.build_release_behavior_tree(),
                self.build_defence_behavior_tree(),
                self.build_ball_is_free_behavior_tree(),
                Action("idle", self.idle)
            )
        )
